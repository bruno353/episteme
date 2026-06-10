---
prd_source: .episteme/prd.md
stepsCompleted: [components, validation-strategy, risks]
status: draft
---
# Architecture Decision Document - artifact validators

Append-only. Each decision carries a confidence tier (uncertain | tentative |
confirmed) and is curated into the ledger. Revise by appending a superseding
decision, never by editing a prior one.

## D-1 - Mirror the existing validator pattern  [confirmed]
verdict-check.py reuses the proven shape of ledger-check.py / policy-check.py:
`argparse` (target path, `--schema`), `jsonschema.Draft202012Validator`, exit
0 (valid) / 1 (problems) / 2 (setup error). A new `schemas/verdict.schema.json`
is the single source of truth for the verdict shape.
- Confidence: **confirmed** - two working validators are direct prior art.
- Ledger: led-0009 (decision, verified).

## D-2 - prd-check parses assumption tags, then cross-checks the ledger  [tentative]
prd-check scans a prd.md for `[ASSUMPTION ...]` tags (regex), extracts each, and
confirms a matching `assumption`/`assumed` ledger entry exists; exit 1 names any
orphan. The EXACT tag grammar is not yet confirmed.
- Confidence: **tentative** - depends on assumption AS-1 (led-0008). Resolve with
  a spike against `templates/prd.md` BEFORE implementing FR-2.
- Ledger: led-0010 (decision, assumed).

## D-3 - No shared validator helper yet  [tentative]
Keep verdict-check / prd-check self-contained; do NOT extract a shared
schema-loading module from ledger-check/policy-check under this feature.
- Confidence: **tentative** - silence over speculation: no measured evidence that
  the ~30 lines of duplication hurt. Revisit only if a third validator makes it real.
- Ledger: led-0011 (decision, assumed).

## C-1 - Pure-local constraint  [confirmed]
Validators make no network or LLM call (led-0007, verified).

## Risks & open questions
- UNKNOWN until the spike (D-2): the precise PRD assumption-tag grammar and whether
  an Assumptions Index is mandatory. prd-check's parser is unspecified until then.
