---
prd_source: .episteme/prd.md
architecture_source: .episteme/architecture.md
status: approved
---
# Epic Breakdown - artifact validators

## Functional requirement inventory
- FR-1 (PRD 4.1): verdict-check validates a verdict.json against a schema.
- FR-2 (PRD 4.2): prd-check confirms every PRD assumption is ledgered.

## Epic 1: Validate verdicts
### story-01: verdict-check + verdict.schema.json
- epic: Epic 1
- Realizes: FR-1
- Acceptance sketch: well-formed verdict -> exit 0; missing-field / bad-kind -> exit 1.
- Risk: none (rests on led-0009 verified).

## Epic 2: Enforce the PRD->ledger through-line
### story-02: [spike] confirm the PRD assumption-tag grammar
- epic: Epic 2
- Realizes: (unblocks FR-2)
- Acceptance sketch: the assumption-tag grammar is confirmed against templates/prd.md and recorded as a verified ledger finding (resolves AS-1 / led-0008).
- Risk: load-bearing for story-03; run first.
### story-03: prd-check
- epic: Epic 2
- Realizes: FR-2
- Acceptance sketch: PRD with all assumptions ledgered -> exit 0; PRD with an orphan assumption -> exit 1.
- Risk: depends on story-02 (assumption grammar). Treat led-0010 as assumed until story-02 verifies it.

## FR coverage map
| FR | Covered by | Note |
|---|---|---|
| FR-1 | story-01 | direct |
| FR-2 | story-03 | story-02 (spike) first to confirm the parse grammar |

Every FR is realized by >=1 story. No FR dropped.
