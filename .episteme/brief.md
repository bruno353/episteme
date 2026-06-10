---
id: brief-artifact-validators
status: active
ledger_seeded: true
---
# Brief: Episteme artifact validators (verdict-check + prd-check)

## Problem

Two of Episteme's own artifacts have no cheap deterministic oracle. `ledger.jsonl`
has `ledger-check.py` and `policy.json` has `policy-check.py`, but `verdict.json` is
unvalidated, and the PRD's "every [ASSUMPTION] is also a ledger entry" through-line
is enforced only by convention. So Pillar 2 (curated memory integrity) and the
fact/hypothesis discipline rest on an honor system for those two artifacts.

## Target users / jobs-to-be-done

- Episteme maintainers: want a one-command check that a verdict / a PRD's assumptions
  are well-formed, mirroring ledger-check/policy-check.
- The loop itself: the verifier/curator voices can call these as the cheap oracle
  instead of eyeballing.

## Goals

- `tools/verdict-check.py` + `schemas/verdict.schema.json`: validate a verdict.json.
- `tools/prd-check.py`: assert every `[ASSUMPTION ...]` in a prd.md has a matching
  `assumption`/`assumed` ledger entry (mechanizes the PRD->ledger through-line).

## Non-goals

- Judging semantic quality (is the verdict/PRD good) - that is the critic, not a checker.
- Any network or LLM call. Pure local validation.
- A validator for every artifact - only the two with no oracle today.

## Known facts (verified)

- `tools/ledger-check.py` and `tools/policy-check.py` exist and are the working
  pattern to mirror (argparse + jsonschema Draft202012Validator + structural checks).
- `jsonschema` is available in the environment (used by the existing validators).

## Assumptions (unverified - to confirm/falsify downstream)

- The PRD assumption convention is an inline tag like `[ASSUMPTION: ...]` plus an
  Assumptions Index section. Must be confirmed against `templates/prd.md` before
  prd-check can parse it reliably (a likely spike).
- A single shared schema-validation helper is worth extracting from the two existing
  validators - unverified; do not refactor them under this feature unless evidence
  shows duplication hurts.
