# Critic report - contract-policy-check (independent post-diff audit)

- **verdict:** approve
- **contradiction_type:** null
- **items_to_revisit:** []
- **suggested_fix:** null

## reasoning

All three audit axes pass against cited evidence. No axis failed.

### Axis 1 - Contract compliance (re-ran all 5 AC oracles verbatim)
Each oracle was executed exactly as written in `contract.md` from the repo root. Every actual exit code matches the contract's expected exit:

- AC-1 `policy-check.py tools/fixtures/policy_good.json` -> exit 0 (expected 0). status=`policy_candidate`.
- AC-2 `policy-check.py tools/fixtures/policy_bad_status.json` -> exit 1 (expected 1). Rejected on `schema [status] 'done' is not one of [...]`. (Fixture deliberately uses out-of-enum `done`.)
- AC-3 `policy-check.py tools/fixtures/policy_missing_field.json` -> exit 1 (expected 1). Rejected on `'readiness_rationale' is a required property`.
- AC-4 `policy-check.py tools/fixtures/policy_ready_unverified.json --ledger tools/fixtures/ledger_for_policy.jsonl` -> exit 1 (expected 1). Rejected because `led-0008` authority is `assumed`; flagged at candidate_steps[0], candidate_steps[1] AND recommended_next_action.
- AC-5 `policy-check.py tools/fixtures/policy_ready_verified.json --ledger tools/fixtures/ledger_for_policy.jsonl` -> exit 0 (expected 0). Every rests_on (led-0007/led-0009) is `verified`.

### Axis 2 - Drift / scope creep
No out-of-scope behavior found. `grep -nE "requests|urllib|socket|http|openai|anthropic|subprocess|os.system|exec(|eval("` over `tools/policy-check.py` => NONE FOUND. The validator imports only argparse/json/sys/pathlib plus a lazy `jsonschema.Draft202012Validator` (mirroring `ledger-check.py`). It validates structure (schema) + the readiness gate (ledger authority lookup) only; it never judges plan SEMANTICS, makes no network/LLM call, and modifies no files. Deliverables touched are exactly the contract's allowed set: `schemas/policy.schema.json`, `tools/policy-check.py`, `tools/fixtures/*`. (Repo is not a git checkout, so "diff" was reviewed as the on-disk files; nothing outside the allowed set was present as new/modified for this feature.)

### Axis 3 - Architecture (led-0004 = verified readiness gate, both axes)
led-0004 requires that a `ready` policy rest only on `verified` ledger entries across BOTH `candidate_steps[].rests_on` AND `recommended_next_action.rests_on`. The code collects pairs from both axes in `_rests_on_ids` (`tools/policy-check.py:37-48`) and checks them in the gate loop (`:114-119`). Adversarial probes (scratch fixtures under /tmp, no repo writes):

- ready policy with clean candidate_steps but `assumed` id (led-0008) ONLY in recommended_next_action -> exit 1 (gate catches the rec-action axis independently). Proves led-0004 is not satisfied by checking candidate_steps alone.
- ready policy resting on an id absent from the ledger (led-9999) -> exit 1 (`absent from the ledger`).
- ready policy with rests_on but `--ledger` omitted -> exit 1 (`cannot prove readiness without the ledger`), matching the error taxonomy.
- valid ready policy with every rests_on verified across both axes -> exit 0 (no false positive).

I could not construct a `ready` policy that wrongly passes, nor a valid one that wrongly fails.

### Additional taxonomy spot-checks
- malformed JSON -> exit 2 with line/col (`Expecting property name ... at line 2 col 3`).
- missing policy file -> exit 2.
- live `.episteme/policy.json` validates -> exit 0 (corroborates led-0005).

## cited_contract_items
- AC-1, AC-2, AC-3, AC-4, AC-5 (all oracles re-run; actual == expected exit)
- Interfaces/surface (exit-code contract 0/1/2; default args) - verified
- Error taxonomy (malformed JSON exit 2; missing --ledger while ready exit 1) - verified
- Out of scope (no semantics validation, no network/LLM, no extra files) - respected

## cited_evidence
- 5/5 AC oracle commands re-run from repo root; exit codes 0,1,1,1,0 == contract.
- `tools/policy-check.py:37-48` (`_rests_on_ids` covers both candidate_steps and recommended_next_action) and `:114-119` (per-pair absent/non-verified check).
- /tmp adversarial fixtures: rec-action-only-unverified=exit1, absent-id=exit1, no-ledger=exit1, all-verified=exit0.
- grep for network/LLM/subprocess/exec in policy-check.py: NONE FOUND.
- Deliverable set on disk = schemas/policy.schema.json + tools/policy-check.py + tools/fixtures/* only.
