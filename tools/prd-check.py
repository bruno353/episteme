#!/usr/bin/env python3
"""Episteme prd-check.

Mechanizes the PRD -> ledger through-line in two checks:

  (A) Every real inline `[ASSUMPTION: <text>]` tag in the PRD must be referenced
      from the `## Assumptions Index` (no orphan inline tags). Implemented as a
      count check: real inline tags must be <= the number of Assumptions Index
      rows that carry a led-NNNN reference. "Real" excludes meta-references like
      the literal `...` placeholder and tags inside backtick code spans.

  (B) Every `led-NNNN` referenced from the Assumptions Index must resolve to a
      `type: "assumption"` entry in the ledger.

Together: an assumption can never sit inline in the PRD without being indexed,
and an indexed assumption can never not be in the ledger.

The tag grammar: inline [ASSUMPTION: <text>] markers plus an '## Assumptions Index' table mapping each assumption to a ledger id.

Usage:
    python3 tools/prd-check.py [path/to/prd.md] --ledger path/to/ledger.jsonl

Exit 0 = all checks pass; 1 = orphan inline tag, or an index ref missing/non-assumption
in the ledger; 2 = setup error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PRD = REPO_ROOT / ".episteme" / "prd.md"
DEFAULT_LEDGER = REPO_ROOT / ".episteme" / "ledger.jsonl"

LED_RE = re.compile(r"led-[0-9]{4,}")
HEADING_RE = re.compile(r"^#{1,6}\s")
# An inline assumption tag: [ASSUMPTION: <text>]. We capture the text payload.
INLINE_TAG_RE = re.compile(r"\[ASSUMPTION:\s*([^\]]+)\]")
# Strip backtick code spans before scanning for inline tags, so meta-references
# like `[ASSUMPTION: ...]` inside docs/templates do not count.
BACKTICK_SPAN_RE = re.compile(r"`[^`]*`")


def _fail(msg: str, code: int = 2) -> int:
    print(f"prd-check: {msg}", file=sys.stderr)
    return code


def _strip_code_spans(text: str) -> str:
    return BACKTICK_SPAN_RE.sub("", text)


def _real_inline_tags(prd_text: str) -> list[str]:
    """Return the payload of each real [ASSUMPTION: ...] tag.

    Skips meta-references: tags inside backtick code spans, and tags whose
    payload is the literal `...` placeholder (literal '...' placeholders are
    meta-references, not real assumptions)."""
    cleaned = _strip_code_spans(prd_text)
    out: list[str] = []
    for payload in INLINE_TAG_RE.findall(cleaned):
        if payload.strip() == "...":
            continue
        out.append(payload.strip())
    return out


def _assumptions_index_refs(prd_text: str) -> list[str]:
    """Collect led-NNNN tokens that appear under an 'Assumptions Index' heading."""
    lines = prd_text.splitlines()
    refs: list[str] = []
    in_section = False
    for line in lines:
        if HEADING_RE.match(line):
            in_section = "assumptions index" in line.lower()
            continue
        if in_section:
            refs.extend(LED_RE.findall(line))
    return refs


def _ledger_types(ledger_path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in ledger_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        entry = json.loads(line)
        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
            out[entry["id"]] = str(entry.get("type", ""))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a PRD's assumptions are ledgered.")
    parser.add_argument("prd", nargs="?", default=str(DEFAULT_PRD),
                        help=f"Path to prd.md (default: {DEFAULT_PRD}).")
    parser.add_argument("--ledger", default=None,
                        help="Path to ledger.jsonl (required).")
    args = parser.parse_args(argv)

    prd_path = Path(args.prd)
    if not prd_path.is_file():
        return _fail(f"prd not found: {prd_path}")
    if not args.ledger:
        return _fail("--ledger is required (cannot check the through-line without the ledger)")
    ledger_path = Path(args.ledger)
    if not ledger_path.is_file():
        return _fail(f"ledger not found: {ledger_path}")

    prd_text = prd_path.read_text(encoding="utf-8")
    inline_tags = _real_inline_tags(prd_text)
    refs = _assumptions_index_refs(prd_text)

    errors: list[str] = []

    # Check A: no orphan inline tags. The Assumptions Index must reference at least
    # as many ledger entries as there are real inline tags.
    if len(inline_tags) > len(refs):
        orphan_n = len(inline_tags) - len(refs)
        sample = "; ".join(t[:60] for t in inline_tags[-orphan_n:])
        errors.append(f"{orphan_n} inline assumption tag(s) not referenced from the "
                      f"Assumptions Index (have {len(inline_tags)} inline tags, "
                      f"{len(refs)} indexed led-refs). Add to the Index: {sample}")

    # Check B: every Assumptions Index led-ref resolves to a `type:assumption` entry.
    if refs:
        try:
            types = _ledger_types(ledger_path)
        except json.JSONDecodeError as exc:
            return _fail(f"invalid JSON in ledger {ledger_path} ({exc.msg} at line {exc.lineno})")
        for ref in refs:
            if ref not in types:
                errors.append(f"Assumptions Index references '{ref}', which is absent from the ledger")
            elif types[ref] != "assumption":
                errors.append(f"Assumptions Index references '{ref}', whose ledger type is "
                              f"'{types[ref]}', not 'assumption'")

    if errors:
        print(f"FAIL: {len(errors)} problem(s) in {prd_path}")
        for e in errors:
            print(f"  - {e}")
        return 1

    if not inline_tags and not refs:
        print(f"OK: no assumption tags or Assumptions Index refs in {prd_path} (nothing to check)")
    else:
        print(f"OK: {len(inline_tags)} inline tag(s) all indexed, "
              f"{len(refs)} Assumptions Index ref(s) all ledgered assumptions in {prd_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
