#!/usr/bin/env python3
"""Episteme policy-check.

Validates a policy.json against schemas/policy.schema.json, then enforces the
readiness gate that the schema cannot express:

    a policy may claim `status: "ready"` ONLY when every ledger id referenced by
    `candidate_steps[].rests_on` and `recommended_next_action.rests_on` exists in
    the ledger AND has authority == "verified".

This is the deterministic oracle for the gated-readiness discipline (Pillar 4),
the policy-side sibling of tools/ledger-check.py.

Usage:
    python3 tools/policy-check.py [path/to/policy.json] [--schema path] [--ledger path]

Exit 0 = valid (and, if ready, gate satisfied); 1 = problems found; 2 = setup error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_POLICY = REPO_ROOT / ".episteme" / "policy.json"
DEFAULT_SCHEMA = REPO_ROOT / "schemas" / "policy.schema.json"
DEFAULT_LEDGER = REPO_ROOT / ".episteme" / "ledger.jsonl"


def _fail(msg: str, code: int = 2) -> int:
    print(f"policy-check: {msg}", file=sys.stderr)
    return code


def _rests_on_ids(policy: dict) -> list[tuple[str, str]]:
    """Return (where, ledger_id) pairs that the readiness gate must check."""
    out: list[tuple[str, str]] = []
    for i, step in enumerate(policy.get("candidate_steps", []) or []):
        if isinstance(step, dict):
            for rid in step.get("rests_on", []) or []:
                out.append((f"candidate_steps[{i}]", str(rid)))
    rec = policy.get("recommended_next_action")
    if isinstance(rec, dict):
        for rid in rec.get("rests_on", []) or []:
            out.append(("recommended_next_action", str(rid)))
    return out


def _load_ledger_authority(ledger_path: Path) -> dict[str, str]:
    """Map ledger id -> authority. Tolerant of blank lines."""
    authority: dict[str, str] = {}
    for raw in ledger_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        entry = json.loads(line)
        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
            authority[entry["id"]] = str(entry.get("authority", ""))
    return authority


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an Episteme policy.json.")
    parser.add_argument("policy", nargs="?", default=str(DEFAULT_POLICY),
                        help=f"Path to policy.json (default: {DEFAULT_POLICY}).")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA),
                        help=f"Path to policy.schema.json (default: {DEFAULT_SCHEMA}).")
    parser.add_argument("--ledger", default=None,
                        help="Path to ledger.jsonl (required when status is 'ready' and steps have rests_on).")
    args = parser.parse_args(argv)

    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return _fail("missing dependency 'jsonschema'. Install with: pip install jsonschema")

    schema_path = Path(args.schema)
    policy_path = Path(args.policy)
    if not schema_path.is_file():
        return _fail(f"schema not found: {schema_path}")
    if not policy_path.is_file():
        return _fail(f"policy not found: {policy_path}")

    try:
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return _fail(f"invalid JSON in {policy_path} ({exc.msg} at line {exc.lineno} col {exc.colno})")

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    errors: list[str] = []
    for err in sorted(validator.iter_errors(policy), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "<root>"
        errors.append(f"schema [{loc}] {err.message}")

    # Readiness gate (only when the policy claims it is ready).
    if policy.get("status") == "ready":
        pairs = _rests_on_ids(policy)
        if pairs:
            if not args.ledger:
                errors.append("status is 'ready' and steps have rests_on, but no --ledger was given; "
                              "cannot prove readiness without the ledger")
            else:
                ledger_path = Path(args.ledger)
                if not ledger_path.is_file():
                    return _fail(f"ledger not found: {ledger_path}")
                try:
                    authority = _load_ledger_authority(ledger_path)
                except json.JSONDecodeError as exc:
                    return _fail(f"invalid JSON in ledger {ledger_path} ({exc.msg} at line {exc.lineno})")
                for where, rid in pairs:
                    if rid not in authority:
                        errors.append(f"readiness gate: {where} rests_on '{rid}', which is absent from the ledger")
                    elif authority[rid] != "verified":
                        errors.append(f"readiness gate: {where} rests_on '{rid}', whose authority is "
                                      f"'{authority[rid]}', not 'verified' - a 'ready' policy may not rest on it")

    if errors:
        print(f"FAIL: {len(errors)} problem(s) in {policy_path} (status={policy.get('status')!r})")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK: policy valid in {policy_path} (status={policy.get('status')!r})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
