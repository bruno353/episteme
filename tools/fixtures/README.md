# Validator fixtures

Oracle fixtures for the deterministic validators in `tools/`. Each line below lists a
validator's fixtures and the exit code it must produce on them - run a validator against
its fixtures to confirm it still behaves as specified.

- **policy-check**: `policy_good.json` = 0; `policy_bad_status.json` = 1; `policy_missing_field.json` = 1; `policy_ready_unverified.json` + `ledger_for_policy.jsonl` = 1; `policy_ready_verified.json` + `ledger_for_policy.jsonl` = 0.
- **verdict-check**: `verdict_good.json` = 0; `verdict_missing_kind.json` = 1; `verdict_bad_kind.json` = 1.
- **prd-check**: `prd_good.md` + `ledger_for_prd.jsonl` = 0; `prd_orphan.md` + `ledger_for_prd.jsonl` = 1; `prd_inline_orphan.md` + `ledger_for_prd.jsonl` = 1.
