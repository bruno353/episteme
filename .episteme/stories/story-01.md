---
id: story-01
epic: Epic 1
realizes: [FR-1]
status: ready-for-dev
contract: null
---
# story-01: verdict-check + verdict.schema.json

As a maintainer, I want a validator for `verdict.json`, so that verdict integrity is
a cheap deterministic check like the ledger and policy already have.

## Acceptance criteria (-> become the contract's oracle-backed ACs)
- AC-1: Given a well-formed verdict.json, when verdict-check runs, then it exits 0.
- AC-2: Given a verdict missing a required field (`kind`), then verdict-check exits 1 naming the field.
- AC-3: Given a verdict whose `kind` is outside the allowed set, then verdict-check exits 1.

## Dev notes
- Mirror `tools/ledger-check.py` / `tools/policy-check.py` (decision led-0009): argparse + jsonschema Draft202012Validator + exit 0/1/2.
- New `schemas/verdict.schema.json`. The verdict shape is in `templates/verdict.json` and METIS Voice 2: `kind` in {passed,failed,mismatch,noop,regression}, plus `reason`, `progress_delta`, `flags`.
- References: [Source: .episteme/architecture.md#D-1], [Source: templates/verdict.json].

## Known facts (verified)
- led-0009: mirror-the-validator-pattern decision is verified (two working validators).
- `templates/verdict.json` exists as the canonical shape.

## Open assumptions
- None material; the verdict shape is observable in the template.
