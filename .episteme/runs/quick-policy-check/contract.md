---
id: contract-policy-check
version: 1
status: active
stories: [dogfood-1]
---
# Contract: policy-check (validator for .episteme/policy.json)

A deterministic validator for the gated-policy artifact, mirroring `ledger-check.py`.
It is the cheap oracle for Pillar-5 on policies: a `policy.json` is structurally
sound, and - crucially - a policy may only claim `status: ready` when every step it
rests on is backed by a `verified` ledger entry. This makes the gated-readiness
discipline mechanically checkable instead of an honor system.

Deliverables: `schemas/policy.schema.json` (JSON Schema, single source of truth) and
`tools/policy-check.py` (Python validator, same shape as `tools/ledger-check.py`).

## Acceptance criteria

- AC-1: A well-formed `policy.json` validates and the tool exits 0.
  - oracle: `python3 tools/policy-check.py tools/fixtures/policy_good.json`
  - expect: exit 0
  - status: red

- AC-2: A policy whose `status` is not one of not_ready/probe_more/policy_candidate/ready is rejected.
  - oracle: `python3 tools/policy-check.py tools/fixtures/policy_bad_status.json`
  - expect: exit 1
  - status: red

- AC-3: A policy missing a required field (`readiness_rationale`) is rejected.
  - oracle: `python3 tools/policy-check.py tools/fixtures/policy_missing_field.json`
  - expect: exit 1
  - status: red

- AC-4: A policy with `status: ready` is rejected when a `candidate_steps[].rests_on`
    id is absent from the ledger OR its ledger authority is `assumed` (the readiness gate).
  - oracle: `python3 tools/policy-check.py tools/fixtures/policy_ready_unverified.json --ledger tools/fixtures/ledger_for_policy.jsonl`
  - expect: exit 1
  - status: red

- AC-5: A policy with `status: ready` whose every `rests_on` id maps to a `verified`
    ledger entry passes.
  - oracle: `python3 tools/policy-check.py tools/fixtures/policy_ready_verified.json --ledger tools/fixtures/ledger_for_policy.jsonl`
  - expect: exit 0
  - status: red

## Interfaces / surface

- `tools/policy-check.py [policy.json] [--schema schemas/policy.schema.json] [--ledger path]`
  - exit 0 = valid (and, if `status: ready`, readiness gate satisfied); exit 1 = problems found; exit 2 = setup error (missing file/dep).
  - prints a human-readable summary (mirror `ledger-check.py` output style).
- `schemas/policy.schema.json` validates a single policy object with at least:
  `status`, `readiness_rationale`, `evidence_audit`, `reachability_audit`,
  `candidate_steps` (each with `action`, `rests_on` array, `stop_or_remeasure_if`),
  `recommended_next_action`.

## Error taxonomy

- malformed JSON -> exit 2 with line/col (setup-ish, but reported clearly).
- schema violation -> exit 1, listing each failing path.
- `status: ready` with an unverified/missing `rests_on` -> exit 1, naming the offending step + id.
- missing `--ledger` while `status: ready` and steps have `rests_on` -> exit 1 (cannot prove readiness without the ledger).

## Out of scope

- Validating policy SEMANTICS (is the plan a good plan) - that is the critic, not this oracle.
- Cross-policy history / retrospective correctness.
- Any network or LLM call. Pure local validation.
