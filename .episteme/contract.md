---
id: contract-prd-check
version: 2
status: active
stories: [story-03]
supersedes_version: 1
---
# Contract: prd-check (PRD assumption -> ledger through-line)

Story-03 / FR-2. Mechanizes the through-line: every assumption a PRD declares must
be ledgered. Per the confirmed grammar (led-0013), prd-check enforces two checks:
(A) every real inline `[ASSUMPTION: <text>]` tag must be referenced from the
`## Assumptions Index` (no orphan inline tags); (B) each Index `led-NNNN` must
resolve to an `assumption`-type entry in the ledger. Deliverable: `tools/prd-check.py`.

**v2 change (from v1):** added AC-3 to close a spine hole flagged by an external
review - v1 only enforced check (B), letting an inline `[ASSUMPTION: ...]` tag pass
without an Index row. v2 enforces (A) too. See ledger led-0016 / led-0017.

## Acceptance criteria

- AC-1: A PRD whose Assumptions Index led-refs all exist as `assumption` ledger entries (and whose inline tags are all indexed) passes.
  - oracle: `python3 tools/prd-check.py tools/fixtures/prd_good.md --ledger tools/fixtures/ledger_for_prd.jsonl`
  - expect: exit 0
  - status: red
- AC-2: A PRD with an Assumptions Index led-ref that is missing from the ledger is rejected.
  - oracle: `python3 tools/prd-check.py tools/fixtures/prd_orphan.md --ledger tools/fixtures/ledger_for_prd.jsonl`
  - expect: exit 1
  - status: red
- AC-3: A PRD with an inline `[ASSUMPTION: <text>]` tag that has no row in the Assumptions Index is rejected.
  - oracle: `python3 tools/prd-check.py tools/fixtures/prd_inline_orphan.md --ledger tools/fixtures/ledger_for_prd.jsonl`
  - expect: exit 1
  - status: red

## Interfaces / surface
- `tools/prd-check.py [prd.md] --ledger path` -> exit 0 all checks pass / 1 an orphan inline or unledgered index ref / 2 setup error. Names the orphan.
- Inline-tag scan ignores backtick code spans and tags whose payload is literally `...` (per led-0013: those are meta-references, not real assumptions).

## Error taxonomy
- missing `--ledger` -> exit 2.
- inline `[ASSUMPTION:]` count exceeds Assumptions Index led-ref count -> exit 1.
- a `led-NNNN` in the Index that is absent from the ledger, or present but not `type: assumption` -> exit 1, naming the ref.

## Out of scope
- Judging whether the assumption is reasonable (semantics).
- Strict text matching between an inline tag and its Index row (count is the v2 oracle; future versions may add tag-id linking).
- Any network/LLM call.
