---
title: Episteme artifact validators
status: active
source_brief: .episteme/brief.md
---
# PRD: Episteme artifact validators (verdict-check + prd-check)

## 1. Vision

Every Episteme artifact that "done" depends on should have a cheap deterministic
oracle. `ledger.jsonl` and `policy.json` already do; this closes the gap for
`verdict.json` and for the PRD's assumption->ledger through-line, so the curated
memory + fact/hypothesis discipline are mechanically enforced, not just convention.

## 2. Target user / Jobs-to-be-done

- Maintainer: "let me confirm a verdict / a PRD's assumptions are well-formed with one command."
- The loop's verifier/curator voices: "use a deterministic gate instead of eyeballing."

## 3. Glossary

- **Verdict**: `.episteme/verdict.json` - the factual result of one verify step.
- **Assumption tag**: an inline `[ASSUMPTION: ...]` marker in a PRD.
- **Ledgered**: an assumption that has a matching `assumption`/`assumed` entry in `.episteme/ledger.jsonl`.

## 4. Features

### 4.1 verdict-check

**Description:** a validator for `verdict.json`, mirroring `ledger-check.py`. Realizes the curated-memory pillar for verdicts.

#### FR-1: verdict-check validates a verdict.json against a schema.
verdict-check exits 0 on a well-formed verdict and exits 1 on a schema violation, naming the failing path.
**Consequences (testable):**
- A well-formed verdict fixture -> exit 0.
- A verdict missing a required field (e.g. `kind`) -> exit 1.
- A verdict whose `kind` is outside the allowed set -> exit 1.

### 4.2 prd-check

**Description:** asserts the PRD->ledger through-line. Realizes the fact/hypothesis pillar at the PRD layer.

#### FR-2: prd-check confirms every PRD assumption is ledgered.
prd-check exits 0 when every `[ASSUMPTION: ...]` tag in a PRD has a matching `assumption`/`assumed` ledger entry, and exits 1 (naming the orphan tag) otherwise.
**Consequences (testable):**
- A PRD whose every assumption tag has a matching ledger entry -> exit 0.
- A PRD with an assumption tag that has no ledger entry -> exit 1.

[ASSUMPTION: the PRD assumption convention is an inline `[ASSUMPTION: ...]` tag plus an Assumptions Index; prd-check parses that grammar. This must be confirmed against `templates/prd.md` before FR-2 is reachable - see Assumptions Index AS-1 / ledger led-0008.]

## 5. Non-goals

- No semantic-quality judgment; no network/LLM (constraint led-0007).
- No validator for artifacts that already have one or that have no "done" dependency.

## 6. Success metrics

- **SM-1**: both validators ship with passing fixtures and are wired into the relevant voices' guidance.
- **Counter-metric (do not optimize)**: number of checks - more validators is not the goal; only the two gaps.

## 7. Assumptions Index

| id | Assumption | Ledger entry | Status |
|---|---|---|---|
| AS-1 | PRD assumption convention is `[ASSUMPTION: ...]` + Assumptions Index | led-0008 | assumed (spike: confirm vs templates/prd.md) |
