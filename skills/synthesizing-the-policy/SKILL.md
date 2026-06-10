---
name: synthesizing-the-policy
description: Use when you have a .episteme/contract.md and a .episteme/ledger.jsonl and need a plan for which change to make next, before writing implementation code - turns KNOWN facts into a gated, advisory candidate plan that refuses to declare "ready" unless every step rests on verified evidence and the contract is provably reachable
---

# Synthesizing the Policy (the gated planner)

## Overview

You read the contract and the curated ledger, and you produce **one advisory plan** -
`.episteme/policy.json` - that says what to do next AND how confident the evidence lets you be.

**Core principle:** A plan is only as trustworthy as the facts under it. You never
promote a plan to `ready` on a hunch; you gate readiness on `verified` ledger entries
and a reachability check, and you hand the implementer exactly one recommended next
action - not a command queue.

**Violating the letter of this rule is violating the spirit of this rule.**

This is Voice 5 of the epistemic loop. You sit **after the contract, before
implementing**. Your `recommended_next_action` is what `implementing-a-story` picks up.

## When to Use

**Use when:**
- A `.episteme/contract.md` exists and enough facts have been gathered into `.episteme/ledger.jsonl`.
- You are about to start (or resume) implementation and need to decide the next change.
- The ledger changed materially (a verdict flipped an oracle, a constraint was found)
  and the prior plan needs reconciling.

**Do NOT use to:**
- Gather facts (that is the fact-gathering step / cheap oracles).
- Write or run a test (that is `implementing-a-story` + `verifying-against-contract`).
- Judge finished code (that is `adversarial-critic`).

You are **advisory only**. You do not edit code, do not run tests, do not declare done.

## The Iron Law

```
NEVER status: "ready" UNLESS EVERY candidate step RESTS ON A `verified` LEDGER ENTRY
AND THE REACHABILITY AUDIT FOUND NO UNRESOLVED BLOCKER.
```

A `target_vector + control_matrix` is a reason to *consider* synthesis, not proof a
plan is ready. The software equivalent: "a contract criterion exists and I have an idea"
is not readiness. Readiness is "the oracle that proves this criterion can be made green
by a step whose mechanism I have already observed working."

## Inputs and output

**Read (do not skip any):**
1. `.episteme/contract.md` - the acceptance criteria, their oracles (red/green), interfaces,
   error taxonomy, out-of-scope. These are the **targets**.
2. `.episteme/ledger.jsonl` - decisions / constraints / findings / assumptions, each
   with `authority` (`verified` | `assumed`), `source`, `created_at_turn`, `supersedes`.
   These are the **facts you build on**.
3. The **prior `.episteme/policy.json`** (if one exists) and what happened since it: which steps
   were executed, the verdicts, which oracle flipped, what regressed.
4. Recent verdicts (`.episteme/verdict.json`) - the freshest contract-oracle state.

**Adaptation from the ARC origin (read this once):** the wmv2 synthesizer planned over a
`target_vector` / `control_matrix` / grid coordinates. Here there are no grids or coords.
The mapping is:

| ARC (wmv2) | Episteme (coding) |
|---|---|
| target_vector components | the contract's acceptance criteria (each with a red/green oracle) |
| control_matrix / controls | the files, functions, modules, and tests you can change |
| measured deltas / action effects | verdicts: an oracle flipping red->green (or green->red) |
| boundary / saturation that no control relieves | a missing capability: a dependency, an interface, a decision not yet made |
| "explore a structurally different mechanism" | "this approach is insufficient; change the design, do not keep tweaking" |

**Produce:** a single `.episteme/policy.json` (schema below; copy `templates/policy.json`).

## The procedure

Work through these in order. Each maps to a field in `.episteme/policy.json`.

### 1. Evidence audit - what do I actually know?

Sort every fact you will rely on into three buckets, by the ledger's `authority` tag:

- **grounded** - backed by a `verified` ledger entry (has an `oracle_ref` or cited
  `evidence_for`). You may build a `ready` step on these.
- **tentative** - `assumed` ledger entries. You may plan around them, but a step that
  depends on one can be at most `policy_candidate`, never `ready`.
- **unknown** - the contract needs it and the ledger is silent. These become
  `discriminators_if_not_ready`.

Never launder an `assumed` entry into a fact. If the ledger says `assumed`, your audit
says tentative, full stop.

### 2. Reachability audit - BEFORE you commit to an approach

This is the step people skip, and it is the one that prevents thrashing. For **each
contract criterion whose oracle is still red**, ask:

> Using only what is **verified** in the ledger, is there a change (or chain of changes)
> to a control I can actually make that flips this oracle green - without hitting a
> blocker that nothing I know about relieves?

- If **every** red criterion has such a path -> `target_reachable: true`, proceed to plan.
- If **any** red criterion is **blocked** - the criterion needs a capability that does
  not exist yet and nothing in the ledger provides it (a missing dependency, an undecided
  interface, an architectural constraint that forbids the obvious move) - then:
  - set `target_reachable: false`,
  - name the blocked criterion AND the blocker in `blocked_components`,
  - name the **missing capability** (the structurally different approach that must
    exist) in `missing_capability`,
  - and make `recommended_next_action` about *acquiring that capability or changing the
    design*, NOT about one more tweak to the blocked approach.

The audit fires **only** when a criterion is *provably* blocked on known facts - not
because you have tried a few times. "I have looped 3 times" is not a reachability signal;
"every move that could flip this oracle is forbidden by a constraint I have verified" is.

<Bad>
reachability_audit: { target_reachable: true }  // never actually checked, just optimistic
candidate_steps: [ "add field", "tweak validator", "tweak validator again", ... ]
// thrashing: the validator can't see the field because the ORM mapping was never added -
// a missing capability that no amount of validator tweaks relieves.
</Bad>

<Good>
reachability_audit: {
  target_reachable: false,
  blocked_components: ["AC-3 (expired tokens rejected): oracle stays red; no verified path"],
  missing_capability: "a clock/now() injection point - the token check reads the system clock directly, so the expiry case is untestable and unreachable without a seam. Change the design to inject time, do not keep editing the check."
}
recommended_next_action: { action: "introduce an injectable time source behind the token verifier", ... }
</Good>

### 3. Previous-policy retrospective - reconcile, do not restart blind

If a prior `.episteme/policy.json` exists, write a short, **factual** retrospective from evidence
only (executed steps, verdicts, oracle flips, what went stale):

- `outcome`: `not_applicable` | `still_live` | `partially_supported` | `needs_patch` |
  `stale` | `contradicted` | `inconclusive`.
- A plan that did not solve the criterion **immediately is not "failed."** Separate
  *still-live* (good, keep going) from *contradicted* (a verdict disproved its premise)
  from *stale* (the state it assumed has moved).
- `carry_forward`: what worked and should survive into this plan.
- `avoid_repeating`: what failed and why, so you do not propose it again.

If the prior policy was contradicted or went stale, you may **not** re-emit `ready` for
the same approach unless you cite **fresh verified evidence** that resolves the issue.

### 4. Candidate steps - short, with stop conditions

Prefer a **short** plan (1-3 steps) where each intermediate state is expected and has a
stop condition, over a long speculative script. For each step:

- `action` - the change to make (a file/function/test, in plain terms - not a diff).
- `expected_effect` - what the cheap oracle should show after (e.g. "AC-2 oracle
  `npm test auth.spec.ts::rejects-expired` flips red->green").
- `stop_or_remeasure_if` - the conditions that mean "stop and re-synthesize" (e.g.
  "if the oracle stays red", "if any green oracle regresses", "if a new constraint
  surfaces").

This is an **advisory worksheet**, not a command queue. The implementer still reads the
live state and picks exactly one change at a time. Do not output a fixed sequence the
harness will execute blindly.

### 5. Recommended next action + the readiness gate

Pick the single best next action and set `status`:

| status | when |
|---|---|
| `not_ready` | key facts are tentative/unknown; the evidence audit has blocking uncertainties. Emit `discriminators_if_not_ready`. |
| `probe_more` | the approach hinges on something you can cheaply verify first (an exploit, an assumption). Name the discriminator that would confirm it. |
| `policy_candidate` | a coherent plan exists but at least one step rests on a tentative (`assumed`) entry, or reachability is uncertain. Plan it, remeasure after each step. |
| `ready` | EVERY step rests on a `verified` entry, reachability passed with no unresolved blocker, the prior-policy retrospective is reconciled, and the expected trace is coherent. |

**Default to `probe_more` or `policy_candidate` early.** `ready` is earned, not assumed.

### 6. Discriminators (when not ready)

When `not_ready` / `probe_more`, do not stall. Emit `discriminators_if_not_ready`: each a
question + the cheap candidate action that would answer it + the expected outcomes. This
is what hands control back to fact-gathering / `implementing-a-story` so the loop makes
progress instead of guessing.

## Discipline (the gates, restated)

- **Never `ready` without all-verified + clean reachability.** (The Iron Law.)
- **Reachability audit BEFORE committing.** If blocked, say "this approach is
  insufficient, change the design" - do not hunt for one more tweak.
- **Reconcile against the prior policy.** No re-`ready` on a contradicted/stale approach
  without fresh verified evidence.
- **Advisory only.** One recommended next action; the implementer picks one change at a
  time. No command queue.
- **Respect epistemic tags.** `assumed` in the ledger -> tentative in your audit ->
  caps the step at `policy_candidate`. Never invert it to fact.
- **Short plans with stop conditions** beat long speculative scripts.
- **A GAME_OVER analogue:** a failing build / red test is NOT progress and NOT
  completion. Never read "the command ran" as "the criterion is met." Only an oracle
  flipping red->green is progress.

## Rationalization table

| Excuse | Reality |
|--------|---------|
| "The criterion exists and I have an idea, so I'm ready" | An idea is not a `verified` mechanism. `policy_candidate` at most. |
| "It's probably reachable" | Run the reachability audit on verified facts. Probably ≠ proven. |
| "The last plan didn't solve it, so it failed - try something totally new" | Separate still-live from contradicted. Don't discard a working approach mid-progress. |
| "I'll list 8 steps so the implementer has the whole path" | Advisory worksheet, not a command queue. Short plan, stop conditions, one action handed over. |
| "This ledger entry is assumed but obviously true" | Then verify it with a discriminator first. `assumed` caps the step. |
| "I've tried 3 times, the approach must be blocked" | Try-count is not a reachability signal. Blocked = a verified constraint forbids every path. |
| "The build ran, so we're closer" | Only an oracle flipping red->green is progress. |

## Red Flags - STOP

- About to emit `ready` while any step rests on an `assumed` entry.
- About to emit `ready` without having written the `reachability_audit`.
- Re-proposing an approach the retrospective marked `contradicted`/`stale` with no new
  evidence.
- A `candidate_steps` list longer than ~3 with no stop conditions (speculative script).
- `discriminators_if_not_ready` empty while status is `not_ready` (stalling).
- Treating a passing-command / no-error as "criterion met."

## Output schema (.episteme/policy.json)

```json
{
  "feature": "contract-<slug>",
  "created_at_turn": 0,
  "status": "not_ready | probe_more | policy_candidate | ready",
  "readiness_rationale": "why the evidence is or is not enough for this status",
  "evidence_audit": {
    "grounded": ["facts backed by a verified ledger entry, cite led-id + oracle"],
    "tentative": ["assumed ledger entries this plan touches, cite led-id"],
    "unknown": ["contract needs it, ledger is silent"],
    "blocking_uncertainties": ["what must be resolved before ready"]
  },
  "reachability_audit": {
    "target_reachable": true,
    "blocked_components": ["red criteria with NO verified path + the blocker, or [] if all reachable"],
    "missing_capability": "if not reachable: the structurally-different approach that must exist (a dependency, an interface seam, a decision); else null"
  },
  "previous_policy_retrospective": {
    "policy_ref": "prior .episteme/policy.json / turn, or null",
    "outcome": "not_applicable | still_live | partially_supported | needs_patch | stale | contradicted | inconclusive",
    "evidence": ["executed steps, verdicts, oracle flips - facts only"],
    "what_worked": ["..."],
    "what_failed_or_went_stale": ["..."],
    "carry_forward": ["..."],
    "avoid_repeating": ["..."]
  },
  "candidate_steps": [
    {
      "action": "the change to make, in plain terms (file/function/test)",
      "expected_effect": "what the cheap oracle should show after, naming the oracle",
      "rests_on": ["led-id(s) this step depends on"],
      "stop_or_remeasure_if": ["conditions that mean stop and re-synthesize"]
    }
  ],
  "recommended_next_action": {
    "action": "the single best next change OR capability to acquire",
    "why": "...",
    "rests_on": ["led-id(s)"],
    "stop_or_remeasure_if": ["..."]
  },
  "discriminators_if_not_ready": [
    {
      "question": "the uncertainty to resolve",
      "candidate_action": "the cheap action that answers it (a grep, a probe test)",
      "expected_outcomes": ["outcome A -> implies X", "outcome B -> implies Y"]
    }
  ],
  "open_questions": ["..."],
  "confidence": "low | medium | high"
}
```

`recommended_next_action` may be `null` only when `status` is `not_ready` and the
discriminators are the next move. Otherwise it is required.

## Verification checklist

Before writing `.episteme/policy.json`:

- [ ] Read `.episteme/contract.md` and `.episteme/ledger.jsonl` this session (not from memory).
- [ ] Every fact relied on is sorted grounded / tentative / unknown by its `authority` tag.
- [ ] The reachability audit is filled in (not defaulted to `true`) and checked against
      verified facts only.
- [ ] If a prior policy exists, the retrospective reconciles it - outcome + carry_forward
      + avoid_repeating.
- [ ] `status: ready` ⇒ every `candidate_steps[].rests_on` points to a `verified` entry
      AND `reachability_audit.target_reachable` is true with empty `blocked_components`.
- [ ] `candidate_steps` is short (≤3) and every step has a `stop_or_remeasure_if`.
- [ ] Exactly one `recommended_next_action` (or null only when `not_ready`).
- [ ] If `not_ready`/`probe_more`, `discriminators_if_not_ready` is non-empty.

Can't check all boxes? You are not done synthesizing. Lower the status or gather more.

## Handoff

`recommended_next_action` -> `implementing-a-story` (the implementer picks one change,
predicts, acts, observes). The `discriminators_if_not_ready` -> the fact-gathering step.
Re-run this skill whenever the ledger changes materially (a verdict flips an oracle, a
new constraint is found, the prior plan is contradicted).
