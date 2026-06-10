---
id: story-03
epic: Epic 2
realizes: [FR-2]
status: ready-for-dev
depends_on: [story-02]
contract: null
---
# story-03: prd-check

As a maintainer, I want a checker that every PRD assumption is ledgered, so that the
fact/hypothesis through-line is enforced, not just a convention.

## Acceptance criteria (-> become the contract's oracle-backed ACs)
- AC-1: Given a PRD whose every assumption tag has a matching `assumption`/`assumed` ledger entry, then prd-check exits 0.
- AC-2: Given a PRD with an assumption tag that has no matching ledger entry, then prd-check exits 1 naming the orphan tag.

## Dev notes
- Mirror the validator pattern (led-0009 shape). Parse assumption tags per the grammar story-02 confirmed; cross-check `.episteme/ledger.jsonl` for a matching `assumption`/`assumed` entry.
- prd-check takes a prd path + `--ledger`.
- References: [Source: .episteme/architecture.md#D-2], [Source: .episteme/epics.md#Epic 2].

## Known facts (verified)
- led-0009: validator pattern verified.

## Open assumptions
- led-0008 / led-0010: the assumption-tag grammar + parse plan. Treated as `assumed`
  until story-02 (spike) verifies it. Do not start this story's contract until story-02 is done.
