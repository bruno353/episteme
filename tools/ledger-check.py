#!/usr/bin/env python3
"""Episteme ledger-check.

Validates a ledger.jsonl (one entry per line) against schemas/ledger.schema.json,
plus structural cross-checks the per-entry schema cannot express:
  - unique ids
  - supersedes targets must reference an id that appears earlier in the file
  - malformed JSON lines reported with line numbers

This is the v1 deterministic oracle for Pillar 2 (curated memory). The SAME schema
file is consumed by the phase-2 Pi (TypeScript) extension - only this runtime is
Python.

Usage:
    python3 tools/ledger-check.py [path/to/ledger.jsonl] [--schema path/to/ledger.schema.json]

Exit code 0 = clean, 1 = problems found, 2 = setup error (missing file / dep).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LEDGER = REPO_ROOT / ".episteme" / "ledger.jsonl"
DEFAULT_SCHEMA = REPO_ROOT / "schemas" / "ledger.schema.json"


def _fail(msg: str, code: int = 2) -> "int":
    print(f"ledger-check: {msg}", file=sys.stderr)
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an Episteme ledger.jsonl.")
    parser.add_argument("ledger", nargs="?", default=str(DEFAULT_LEDGER),
                        help=f"Path to ledger.jsonl (default: {DEFAULT_LEDGER}).")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA),
                        help=f"Path to ledger.schema.json (default: {DEFAULT_SCHEMA}).")
    args = parser.parse_args(argv)

    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return _fail("missing dependency 'jsonschema'. Install with: pip install jsonschema")

    schema_path = Path(args.schema)
    ledger_path = Path(args.ledger)
    if not schema_path.is_file():
        return _fail(f"schema not found: {schema_path}")
    if not ledger_path.is_file():
        return _fail(f"ledger not found: {ledger_path} (nothing to check yet?)")

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    errors: list[str] = []
    seen_ids: dict[str, int] = {}        # id -> line number
    supersedes: list[tuple[int, str, str]] = []  # (line, this_id, target_id)

    for lineno, raw in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"L{lineno}: invalid JSON ({exc.msg} at col {exc.colno})")
            continue

        for err in sorted(validator.iter_errors(entry), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in err.path) or "<root>"
            errors.append(f"L{lineno}: schema [{loc}] {err.message}")

        entry_id = entry.get("id")
        if isinstance(entry_id, str):
            if entry_id in seen_ids:
                errors.append(f"L{lineno}: duplicate id '{entry_id}' (first seen L{seen_ids[entry_id]})")
            else:
                seen_ids[entry_id] = lineno
        sup = entry.get("supersedes")
        if isinstance(sup, str) and isinstance(entry_id, str):
            supersedes.append((lineno, entry_id, sup))

    for lineno, this_id, target in supersedes:
        if target not in seen_ids:
            errors.append(f"L{lineno}: '{this_id}' supersedes unknown id '{target}'")
        elif seen_ids[target] >= lineno:
            errors.append(f"L{lineno}: '{this_id}' supersedes '{target}' which appears later (L{seen_ids[target]}); supersede only earlier entries")

    if errors:
        print(f"FAIL: {len(errors)} problem(s) in {ledger_path} ({len(seen_ids)} entries scanned)")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK: {len(seen_ids)} entries valid in {ledger_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
