#!/usr/bin/env python3
"""Episteme verdict-check.

Validates a verdict.json against schemas/verdict.schema.json. The verdict-side
sibling of ledger-check.py / policy-check.py - the cheap deterministic oracle for
the verdict artifact (Pillar 4, right-oracle doctrine).

Usage:
    python3 tools/verdict-check.py [path/to/verdict.json] [--schema path]

Exit 0 = valid; 1 = problems found; 2 = setup error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VERDICT = REPO_ROOT / ".episteme" / "verdict.json"
DEFAULT_SCHEMA = REPO_ROOT / "schemas" / "verdict.schema.json"


def _fail(msg: str, code: int = 2) -> int:
    print(f"verdict-check: {msg}", file=sys.stderr)
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an Episteme verdict.json.")
    parser.add_argument("verdict", nargs="?", default=str(DEFAULT_VERDICT),
                        help=f"Path to verdict.json (default: {DEFAULT_VERDICT}).")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA),
                        help=f"Path to verdict.schema.json (default: {DEFAULT_SCHEMA}).")
    args = parser.parse_args(argv)

    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return _fail("missing dependency 'jsonschema'. Install with: pip install jsonschema")

    schema_path = Path(args.schema)
    verdict_path = Path(args.verdict)
    if not schema_path.is_file():
        return _fail(f"schema not found: {schema_path}")
    if not verdict_path.is_file():
        return _fail(f"verdict not found: {verdict_path}")

    try:
        verdict = json.loads(verdict_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return _fail(f"invalid JSON in {verdict_path} ({exc.msg} at line {exc.lineno} col {exc.colno})")

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    errors: list[str] = []
    for err in sorted(validator.iter_errors(verdict), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "<root>"
        errors.append(f"schema [{loc}] {err.message}")

    if errors:
        print(f"FAIL: {len(errors)} problem(s) in {verdict_path} (kind={verdict.get('kind')!r})")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK: verdict valid in {verdict_path} (kind={verdict.get('kind')!r})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
