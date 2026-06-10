---
id: story-02
epic: Epic 2
realizes: []
type: spike
status: ready-for-dev
contract: null
---
# story-02: [spike] confirm the PRD assumption-tag grammar

A spike, not a behavior story. Its "done" is a recorded ledger finding, not a passing
test (see develop's "Spike stories" branch).

## Discriminator question
What is the actual assumption-tag grammar used by Episteme PRDs - is led-0008's guess
(`[ASSUMPTION: ...]` inline + an Assumptions Index) correct against `templates/prd.md`
and `.episteme/prd.md`? prd-check (story-03) cannot be written reliably until this is known.

## How to resolve
Read `templates/prd.md` and `.episteme/prd.md`; record the real tag grammar as a
`finding`. If it matches led-0008, supersede led-0008 with a `verified` finding; if it
differs, record the corrected grammar (and supersede led-0010 if its parse plan changes).

## Done (spike oracle = the ledger gate)
- The grammar is recorded as a `verified` ledger finding, and `ledger-check` is clean.
- No contract, no policy, no critic diff pass.

## Known facts (verified) / Open assumptions
- led-0008 (assumed): the grammar guess - this spike confirms or corrects it.
