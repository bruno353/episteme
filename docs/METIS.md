# Metis - the architecture (spec, v0.1)

**METIS = Multi-agent Epistemic Typed-ledger Investigation Synthesis** - the reasoning
architecture that Episteme runs on. Episteme is the framework; Metis is the loop inside it.

> Metis is distilled from `world_model_agent_v2`, our ARC-AGI-3 research agent -
> but it is an **adaptation, not a copy**. ARC has no cheap oracle at runtime;
> software does (tests, types, lint, CI). So wherever wmv2 had to invent an
> expensive proxy, we lean on the cheap oracle instead, and keep only the
> epistemic discipline that still earns its place. Skill names never carry
> "metis" - they live in the `episteme:` namespace.

This is the voice-by-voice spec of the loop. Each voice below ships as an
`episteme:` skill.

---

## The two durable artifacts

Everything below reads from and writes to two files. They are the source of truth;
the voices are just disciplined readers/writers of them.

### 1. `contract.md` (one per feature)
The verifiable spec. "Done" is judged against this, not against the agent's word.
Each acceptance criterion is **paired with its cheap oracle**, and that oracle (the
failing test) is authored from the contract *blind to the implementation* - this is
the "two agents that don't see each other" separation (oracle-author vs implementer).

```markdown
---
id: contract-<feature-slug>
version: 3
status: draft | active | satisfied
stories: [story-12, story-13]
---
# Contract: <feature name>

## Acceptance criteria
- AC-1: <human-readable criterion>
  - oracle: `npm test -- auth.spec.ts::rejects-expired-token`   # how we verify it
  - status: red | green
- AC-2: ...

## Interfaces / surface
<public functions, endpoints, types this feature must expose>

## Error taxonomy
<the failure cases that must be handled, each ideally with an oracle>

## Out of scope
<explicit non-goals - bounds the critic>
```

The critic checks story-vs-contract drift; the curator versions the contract in
the ledger when it changes.

### 2. `ledger.jsonl` (one per project/feature) - typed, append-only
Curated memory. Written by the agent and validated by a deterministic gate:
`schemas/ledger.schema.json` is the source of truth and `tools/ledger-check.py`
enforces it (schema + unique ids + supersedes chain). One JSON object per line:

```json
{"id":"led-0007","type":"decision","statement":"auth uses short-lived JWT + refresh, not sessions","source":"story-12 brainstorm","authority":"verified","oracle_ref":"npm test auth.spec.ts","created_at_turn":14,"supersedes":null,"evidence_for":["ADR-2","test green"],"evidence_against":[]}
{"id":"led-0008","type":"constraint","statement":"refresh endpoint must be rate-limited","source":"contract AC-4","authority":"assumed","created_at_turn":14}
{"id":"led-0009","type":"finding","statement":"existing UserService already hashes with argon2","source":"grep src/users","authority":"verified","created_at_turn":15}
```

Entry types: `decision` | `constraint` | `finding` | `assumption` | `contract_version`.
Every entry carries **source**, **authority** (`verified` = an oracle/observation
backs it; `assumed` = inferred, not yet verified), and **freshness** (`created_at_turn`,
`supersedes`). This is Pillar 2 + Pillar 3 made concrete: the ledger never lets a
hypothesis silently become a fact - it is tagged `assumed` until an oracle flips it
to `verified`.

---

## The loop (`episteme:develop`, the orchestrator)

```
gather facts  ->  separate fact/hypothesis  ->  write/confirm contract (+ author oracles, blind)  ->
synthesize gated policy  ->  implement (predict->act->observe)  ->
verdict (cheap oracle)  ->  adversarial critic vs contract  ->  curate ledger
        ^                                                                |
        +----------------------------- repeat until contract all-green --+
```

The loop is the happy path. Each voice below is also a standalone `episteme:` skill
you can invoke alone (e.g. run the critic on existing code without the full loop).

---

## The 5 voices

### Voice 1 - Implementer  (`episteme:implementing-a-story`)
- **wmv2 origin:** Tactical Reasoner (`reasoner.py`). One LLM call/turn -> one typed `AgentTurn`.
- **Adaptation:** one *code change* at a time, TDD-style predict -> act -> observe. Drop grid/coords/ACTION6; keep "one action, schema-strict, observe before re-planning, no blind execution".
- **Reads:** the contract criterion in play, the ledger (decisions/constraints/findings + the last verdict), the policy (if a gated plan exists), the codebase.
- **Produces (a typed turn):** `belief` (current state of the work), `hypothesis_id`, `next_change` (the diff to make), `prediction` (what the oracle should show after), `expected_invariant` (the testable assertion), `confidence`.
- **Discipline:** exactly ONE change per turn; never silently swallow a malformed step (fail loud, let the loop retry); always read the last verdict before re-planning; if the invariant is unfalsifiable, demote to "explore" rather than commit to it.
- **Failure modes guarded:** blind execution (acting without reading the prior verdict), multi-step batching that hides which change caused what.
- **Cadence:** every turn.

### Voice 2 - Verifier  (`episteme:verifying-against-contract`)
- **wmv2 origin:** Verifier (`verifier.py`). Emits a factual `Verdict`, separates "prediction held (fact)" from "progress toward the objective".
- **Adaptation:** the verdict runs the **cheap oracle** (test/type/lint/command). Drop pixel-diff/bbox/grid-signature; keep the fact/progress separation and orthogonal flags.
- **Reads:** the executed change, before/after state, the implementer's `prediction` + `expected_invariant`, and the oracle output.
- **Produces:** `Verdict { kind: passed | failed | mismatch | noop | regression, reason, invalidates_hypothesis, progress_delta, flags }`. **`progress_delta` reflects ONLY contract-oracle state**: +1 when a contract criterion's oracle flips red->green, -1 when a green one regresses, 0 otherwise. Flags: `ORACLE_PASSED`, `ORACLE_FAILED`, `PREDICTION_MISMATCH`, `REGRESSION`, `STATE_REVISITED` (loop). A passing oracle the implementer did NOT predict is a `mismatch`, not a pass.
- **Discipline (the key one):** `"confirmed"` means *the prediction held* (a fact), NOT *we're closer to done*. The oracle going green is the only thing that moves `progress_delta`. The verifier never says "this is good code" - that is the critic's lens.
- **Failure modes guarded:** loops (same change/state revisited), redundant no-op changes (pre-check can block before executing).
- **Cadence:** pre-change (can block) + post-change (judge).

### Voice 3 - Critic  (`episteme:adversarial-critic`)
- **wmv2 origin:** Plan Critic (`plan_critic.py`) - which audits the Curator's `strategic_intent`, default-approve, rejects only with cited evidence, anti-deadlock cap.
- **Adaptation (deliberate):** in wmv2 the critic audits the *plan/intent*. Here it is a **post-diff reviewer** that reads the **contract** and audits the diff against it for compliance, drift, and architecture - reading the contract + ledger + diff, never the implementer's private reasoning. The "two agents that don't see each other" principle does NOT live here: that is the oracle-author (writes tests from the contract, blind to the implementation) vs the implementer. The verifier just runs the pre-authored oracle; the critic is a separate, later, qualitative check where no cheap oracle exists (compliance/drift/architecture).
- **Reads:** the contract, the ledger (consolidated decisions/constraints + epistemic tags), the diff or proposed approach, the verifier's verdicts. NOT the implementer's chain-of-thought.
- **Produces:** `CriticVerdict { verdict: approve | reject, reasoning (names which axis failed), cited_contract_items, cited_evidence, contradiction_type, suggested_fix (what to reconsider, not a replacement), items_to_revisit }`.
- **Discipline:** default-approve - reject ONLY with cited evidence, never vague intuition; anti-deadlock - max 2 consecutive rejections of the same signature, then force-approve; re-audit when the facts materially changed; respect epistemic tags (never treat an `assumed` ledger entry as `verified`); flag contract-vs-work drift; reject "future-step script leak" (an approach that hard-codes a fixed action sequence instead of a decision policy).
- **Failure modes guarded:** rubber-stamping (the audit axes) and deadlock (the cap).
- **Cadence:** on a new approach, on a completion claim, or when the ledger facts changed.

### Voice 4 - Curator  (`episteme:curating-the-ledger`)
- **wmv2 origin:** Knowledge Curator (`knowledge_curator.py`). Sole owner of consolidated knowledge; stable, amends-not-rewrites; carries the MEASURED/HYPOTHESIS discipline.
- **Adaptation:** sole owner of `ledger.jsonl`. Drop grid mechanical-rules/coords; keep authority tagging (verified vs assumed), carry-forward, amend-not-overwrite, context-priority, competing-interpretations-alive, failed-ideas-with-reopen-condition.
- **Reads:** the ledger so far, recent turns/verdicts/diffs, the contract, the critic's rejections (`items_to_revisit`), the codebase facts.
- **Produces:** appended ledger entries (the typed JSONL above) + an optional `strategic_intent` (current approach as a *relation/policy*, never a click-by-click script). Versions the contract into a `contract_version` entry when it changes.
- **Discipline:** promote an entry to `verified` only with an oracle/repeated evidence (one observation is not a rule); carry forward prior entries unless contradicted; never fabricate or invert a finding; mark source + authority on EVERY entry; keep competing interpretations alive instead of collapsing to one; track failed ideas with *why* and *what would reopen them*; current facts outrank old summaries; run an integrity-check pass over the JSONL (re-read, validate shape) since there's no runtime validator in v1.
- **Failure modes guarded:** hypothesis-becomes-fact (authority tags), stale memory (freshness/supersedes), rewrite-churn (amend, don't overwrite), critic-bypass (must actually reconsider `items_to_revisit`, not re-assert).
- **Cadence:** every N turns or on context change (feature/story boundary).

### Voice 5 - Policy-synthesis  (`episteme:synthesizing-the-policy`)
- **wmv2 origin:** Operational Policy Synthesizer (`operational_policy.py`). Turns measured evidence into a gated advisory plan.
- **Adaptation:** turns the ledger's known facts into a candidate implementation plan, but **gates readiness**. Drop target_vector/control_matrix/coords; keep the readiness states, the reachability audit, the prior-policy retrospective, and the discriminators.
- **Reads:** the ledger (facts/constraints/findings), the contract, the prior policy + its execution context (what was done since, with verdicts/effects), recent verdicts.
- **Produces:** `PolicyReport { status: not_ready | probe_more | policy_candidate | ready, readiness_rationale, evidence_audit (what's grounded/tentative/unknown), reachability_audit (is the contract reachable with what is known? if blocked, name the missing capability), previous_policy_retrospective (what worked / went stale, carry_forward, avoid_repeating), candidate_steps (each with expected effect + stop/remeasure condition), recommended_next_action, discriminators_if_not_ready }`.
- **Discipline:** never `ready` unless every step rests on a `verified` ledger entry and no unresolved blocker remains; do a reachability audit on known facts *before* committing - if a criterion is blocked with no known path, say "this approach is insufficient, explore a structurally different one" instead of hunting for one more tweak; reconcile against the prior policy's retrospective; advisory only (never a command queue - the implementer still picks one change at a time); prefer short candidate plans with stop conditions over long speculative scripts.
- **Failure modes guarded:** committing to an evidence-unsupported plan and then thrashing (the readiness gate), repeating a failed approach (the retrospective).
- **Cadence:** once enough facts are gathered; refreshed as the ledger changes.

---

## The two folded voices (not standalone skills in v1)

- **Investigator** (wmv2 `investigator.py`, the read-only measurement workspace) -> folded into the **fact-gathering step** of the loop. In code, the cheap oracles ARE the measurement: run the tests, the type-checker, `grep`/read the code. Findings get written to the ledger as `verified` entries. We do not need a separate "measurement" voice because the oracle is cheap and direct.
- **Theorist** (wmv2 `world_model_theorist.py`, the slow game-structure model) -> folded into the **architecture skill** (full track). It is the slowly-evolving model of the codebase/domain, with confidence tiers and "silence over speculation". It does not run in the Quick track.

Both can be promoted to standalone skills later if a real need appears (Pillar:
don't add ceremony before it earns its place).

---

## What we deliberately dropped from ARC (honesty log)

- Grids, pixels, coordinates, `ACTION6`, color IDs, bbox/diff-region matching - all ARC perception machinery. Our "observation" is the codebase + oracle output.
- `progress_delta` as level-state -> reframed as contract-oracle state (criterion red/green).
- The verifier's mutual-reversal/grid-signature loop detection -> kept the *idea* (loop detection) but the signal is "same diff/test state revisited", not pixel signatures.
- The whole "no cheap oracle, so push every judgment to the LLM" stance **inverts**: in code we WANT the cheap deterministic gate (test/type/lint) as the trust spine, and reserve the LLM for where no oracle exists (design, contract-compliance, approach soundness). This is Pillar 4.
