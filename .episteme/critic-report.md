---
role: adversarial-critic
contract: contract-prd-check
contract_version: 2
audit_target: v2 hardening of tools/prd-check.py + schemas/verdict.schema.json + tools/fixtures/prd_inline_orphan.md
created_at_turn: 5
supersedes: .episteme/runs/* (v1 critic report archived there)
---

# Critic report - v2 hardening audit (prd-check + verdict.schema)

## verdict
**approve**

## reasoning
Independent post-diff audit. All four axes pass with cited evidence: (1) the three v2 AC oracles from `.episteme/contract.md` reproduce exit 0 / 1 / 1 verbatim and the AC-3 failure message names the orphan; (2) the hardening genuinely closes the v1 hole - two adversarial fixtures confirm `_real_inline_tags` correctly skips the literal `...` meta-reference and backtick-wrapped tags, so neither bloats the count; (3) the verdict schema now rejects a verdict missing only `progress_delta` and rejects an unknown flag `WHATEVER`, while the live `.episteme/verdict.json` still validates (no regression); (4) `tools/prd-check.py` imports only stdlib (argparse / json / re / sys / pathlib) - no network, no LLM, no out-of-scope file touches, honoring led-0007. The audited diff stays inside the three files declared in led-0017 and led-0018.

## cited_contract_items
- contract-prd-check v2 AC-1 (`.episteme/contract.md` lines 22-25): exit 0 on `tools/fixtures/prd_good.md`.
- contract-prd-check v2 AC-2 (lines 26-29): exit 1 on `tools/fixtures/prd_orphan.md`.
- contract-prd-check v2 AC-3 (lines 30-33): exit 1 on `tools/fixtures/prd_inline_orphan.md`.
- Interface clause (line 37): "Inline-tag scan ignores backtick code spans and tags whose payload is literally `...`."
- Error taxonomy (line 41): "inline `[ASSUMPTION:]` count exceeds Assumptions Index led-ref count -> exit 1."
- led-0007 pure-local constraint: no network/LLM calls in validators.
- led-0016 (contract bump to v2), led-0017 (prd-check hardening claim), led-0018 (verdict schema hardening claim).

## cited_evidence

### Axis 1 - re-run all 3 AC oracles verbatim

```
$ python3 tools/prd-check.py tools/fixtures/prd_good.md --ledger tools/fixtures/ledger_for_prd.jsonl
OK: 1 inline tag(s) all indexed, 1 Assumptions Index ref(s) all ledgered assumptions in tools/fixtures/prd_good.md
EXIT=0   # AC-1 expected 0 -> MATCH

$ python3 tools/prd-check.py tools/fixtures/prd_orphan.md --ledger tools/fixtures/ledger_for_prd.jsonl
FAIL: 1 problem(s) in tools/fixtures/prd_orphan.md
  - Assumptions Index references 'led-0999', which is absent from the ledger
EXIT=1   # AC-2 expected 1 -> MATCH (names the orphan ref)

$ python3 tools/prd-check.py tools/fixtures/prd_inline_orphan.md --ledger tools/fixtures/ledger_for_prd.jsonl
FAIL: 1 problem(s) in tools/fixtures/prd_inline_orphan.md
  - 1 inline assumption tag(s) not referenced from the Assumptions Index (have 2 inline tags, 1 indexed led-refs). Add to the Index: there is a second untracked bet here, and it has no Index ro
EXIT=1   # AC-3 expected 1 -> MATCH (names the orphan inline-tag payload, truncated at 60 chars)
```

### Axis 2 - the hardening actually closes the hole

Adversarial fixture A: literal `...` meta-reference + 1 real inline + 1 indexed row.
`/tmp/prd_meta_ref.md`.

```
$ python3 tools/prd-check.py /tmp/prd_meta_ref.md --ledger tools/fixtures/ledger_for_prd.jsonl
OK: 1 inline tag(s) all indexed, 1 Assumptions Index ref(s) all ledgered assumptions in /tmp/prd_meta_ref.md
EXIT=0   # The literal '...' was correctly excluded; only the real tag counted (1, not 2).
```

Adversarial fixture B: inline tag wrapped in backticks (`/tmp/prd_backtick.md`).

```
$ python3 tools/prd-check.py /tmp/prd_backtick.md --ledger tools/fixtures/ledger_for_prd.jsonl
OK: no assumption tags or Assumptions Index refs in /tmp/prd_backtick.md (nothing to check)
EXIT=0   # BACKTICK_SPAN_RE correctly stripped the code span; 0 real inline tags counted.
```

Both meta-reference forms documented in the contract (literal `...` payload AND backtick code spans) are demonstrably honored.

### Axis 3 - verdict schema hardening sufficient + non-regressive

Adversarial verdict missing only `progress_delta`:
```
$ python3 tools/verdict-check.py /tmp/verdict_missing_progress_delta.json
FAIL: 1 problem(s) in /tmp/verdict_missing_progress_delta.json (kind='passed')
  - schema [<root>] 'progress_delta' is a required property
EXIT=1   # Names exactly the missing field.
```

Adversarial verdict with invalid flag `WHATEVER`:
```
$ python3 tools/verdict-check.py /tmp/verdict_bad_flag.json
FAIL: 1 problem(s) in /tmp/verdict_bad_flag.json (kind='passed')
  - schema [flags/1] 'WHATEVER' is not one of ['ORACLE_PASSED', 'ORACLE_FAILED', 'PREDICTION_MISMATCH', 'REGRESSION', 'STATE_REVISITED']
EXIT=1   # Closed enum rejects unknown flag values.
```

Regression check on the live verdict:
```
$ python3 tools/verdict-check.py .episteme/verdict.json
OK: verdict valid in .episteme/verdict.json (kind='passed')
EXIT=0   # No regression introduced by the tightened required-fields list.
```

### Axis 4 - architecture / scope (led-0007 pure-local)

```
$ grep -nE '^(import|from)\s' tools/prd-check.py
26:from __future__ import annotations
28:import argparse
29:import json
30:import re
31:import sys
32:from pathlib import Path

$ grep -nE 'requests|urllib|openai|anthropic|httpx|aiohttp|socket' tools/prd-check.py
(no matches; grep exit 1)
```

Stdlib only. No network, no LLM client, no subprocess shelling out to one. The audited diff touches only `tools/prd-check.py`, `schemas/verdict.schema.json`, and `tools/fixtures/prd_inline_orphan.md`, matching the scope declared in led-0017 / led-0018.

## contradiction_type
null

## suggested_fix
null

## items_to_revisit
- (non-blocking, v3 candidate) Check A is purely count-based: `len(inline_tags) > len(refs) -> orphan`. It does not catch a symmetric case where counts match but the indexed rows describe different bets than the inline ones (text mismatch). The contract explicitly defers this to "future versions ... tag-id linking" (line 46), so this is out of scope for v2 and does NOT block approval. Flag it whenever v3 is opened.
- (non-blocking, cosmetic) The orphan-naming code prints `inline_tags[-orphan_n:]`, i.e. the LAST N tags in document order. When the real orphan is the first tag in the document, the printed sample would name the wrong tag while still correctly counting the gap. The contract only requires "Names the orphan" loosely (line 36); acceptable for v2, worth tightening when tag-id linking lands.
