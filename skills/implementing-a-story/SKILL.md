---
name: implementing-a-story
description: Use when implementing against an Episteme contract - turning a contract criterion + .episteme/policy.json recommended_next_action into code, one change at a time. Each turn predicts what the oracle will show, makes exactly ONE change, then hands to verifying-against-contract and reads the verdict before the next change. Triggers when you have an active .episteme/contract.md + .episteme/ledger.jsonl and are about to write or edit code.
---

# Implementing a Story (the Implementer voice)

## Overview

You are the **Implementer** - Voice 1 of the Episteme loop. Your cadence is **every
turn**. Your job is not to "build the feature"; it is to make **one falsifiable code
change**, predict what the cheap oracle will show, and let the verdict - not your own
confidence - decide whether you were right.

This is the wmv2 Tactical Reasoner adapted to code: one LLM call -> one typed turn ->
ONE action -> observe the verdict before re-planning. In ARC the action was a grid
click; here it is a **single code change**. The discipline transfers exactly; the
substrate changes. There are no grids, coordinates, or `ACTION6` here - drop all of it.

**Core principle:** If you cannot state what the oracle will show *before* you change
the code, you do not understand the change well enough to make it. Stop and gather facts.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
ONE CODE CHANGE PER TURN, WITH A PREDICTED ORACLE OUTCOME,
THEN VERIFY BEFORE THE NEXT CHANGE
```

No batching. No "I'll fix these three things while I'm in here." No claiming a criterion
is done without an oracle run. No re-planning until you have read the last verdict.

Broke the law? The change does not count. Revert to the last green oracle state and
start the turn over.

## When to Use

**Always**, on any turn where you are about to write or edit code inside the loop:
- A new acceptance criterion is `red` and needs implementation
- A verdict came back `failed` / `mismatch` / `regression` and needs a corrective change
- A refactor is needed to keep a green criterion green

**Position in the loop:** you run *after* `synthesizing-the-policy` (which hands you a
`recommended_next_action`) and *before* `verifying-against-contract` (which runs the
oracle and returns a verdict). Each of your turns pairs 1:1 with a verifier turn.

Thinking "this change is too small to predict / too obvious to verify"? Stop. That is
the rationalization the verdict exists to catch.

## The Turn (read -> predict -> change -> hand off -> observe)

```
1. READ      contract criterion in play + recommended_next_action + ledger + last verdict
2. PREDICT   what the oracle will show AFTER this change (the prediction)
             + the testable assertion that must hold (the expected_invariant)
3. CHANGE    make exactly ONE code change toward that criterion - nothing more
4. HAND OFF  to verifying-against-contract (run the cheap oracle)
5. OBSERVE   read the verdict in full BEFORE planning the next change
```

### 1. READ - assemble your inputs (do not skip any)

You read four things, in this order. If any is missing, that is itself a signal.

| Input | Where | What you take from it |
|---|---|---|
| The contract criterion **in play** | `.episteme/contract.md` (one AC) | the exact behavior + its paired oracle command |
| `recommended_next_action` | `.episteme/policy.json` (from policy-synthesis) | the advised single step (advisory, not a command) |
| The ledger | `.episteme/ledger.jsonl` | decisions/constraints/findings - respect `authority` tags |
| The **last verdict** | `.episteme/verdict.json` (from the prior turn) | did the previous change do what was predicted? |

- The policy is **advisory**. You still pick exactly one change. If the policy's
  `recommended_next_action` is not the highest-leverage single step given the last
  verdict, deviate - and say why in your turn record.
- Respect epistemic tags. A ledger entry tagged `assumed` is a hypothesis, not a fact.
  Do not write code that *depends* on an `assumed` entry being true; if you must, your
  prediction is a probe to verify it, and your `confidence` is low.
- If there is **no last verdict yet** (first turn of the story), that is fine - but you
  cannot have re-planned off a verdict you never read on later turns.

### 2. PREDICT - state the oracle outcome before you touch code

This is the TDD red step, generalized. The oracle is whatever the contract pairs with
the criterion: a failing test, a type-check, a lint rule, a build, a command exit code.

State two things, concretely:

- **`prediction`** - what the oracle output will be *after* the change. Name the oracle
  and the observable result. "`npm test -- auth.spec.ts::rejects-expired-token` flips
  red -> green; 0 other failures."
- **`expected_invariant`** - the single testable assertion the change must make true.
  "An expired JWT yields HTTP 401 with body `{error:'token_expired'}`."

<Good>
```
prediction: "`pnpm test cart.spec.ts::applies-percent-discount` goes red->green,
             suite stays 41/41, no new type errors."
expected_invariant: "cart.total === subtotal * (1 - discountRate) for a valid code"
```
Names the exact oracle, the exact transition, one assertion.
</Good>

<Bad>
```
prediction: "the discount logic should work now"
expected_invariant: "the cart behaves correctly"
```
Unfalsifiable. "Should" and "correctly" cannot be checked by an oracle. This is the
unfalsifiable-invariant trap (see below) - demote to explore, do not commit to it.
</Bad>

**If you cannot predict the oracle outcome, do NOT guess and change code.** That is the
signal to gather facts first: read the failing test, `grep` the call site, read the
type. Inability to predict is information - it means a fact is missing from the ledger,
not that you should try something and see. (In wmv2 terms: an unfalsifiable invariant is
demoted to `explore_only` rather than credited as progress. Same move here.)

### 3. CHANGE - exactly one change toward this criterion

Make the smallest change that could make your prediction come true. Scope discipline is
non-negotiable:

- Touch only what *this* criterion needs. No drive-by renames, no "while I'm here"
  refactors, no fixing an unrelated lint warning. The adversarial critic reads the
  contract and will reject scope drift with cited evidence - do not hand it the drift.
- Minimal, not clever. The verdict rewards the oracle going green, not elegance. Clean
  up in a separate, predicted refactor turn *after* it is green.
- If making "one change" honestly requires editing three files (e.g. a signature +
  its two callers), that is still ONE change *iff* it is a single indivisible step
  toward one criterion. The test: could a verdict attribute a failure unambiguously to
  this change? If two unrelated behaviors moved, you batched - split it.

<Good>
Criterion AC-3 needs expired-token rejection. You add the expiry check in
`verifyToken()` and nothing else. One behavior moved.
</Good>

<Bad>
While adding the expiry check you also "tidy" the logger, rename `usr` to `user`
across the file, and bump a dependency. Now a red verdict cannot tell you which edit
broke it.
</Bad>

### 4. HAND OFF - run the cheap oracle (verifying-against-contract)

You do not judge your own change. Invoke `verifying-against-contract`, which runs the
contract's oracle for this criterion and returns a typed `Verdict`. Right-oracle
doctrine (Pillar 4): the deterministic gate - test/type/lint/build - is the trust spine
here, *because code has one*. Reserve LLM judgment for the critic (compliance/drift),
not for deciding whether your own code passed.

**Never claim the criterion is satisfied on your own word.** "I implemented it" is not
"the oracle is green." Only the verdict closes a criterion.

### 5. OBSERVE - read the verdict before re-planning

The verdict comes back as `{ kind, reason, invalidates_hypothesis, progress_delta, flags }`.
Read it **in full** before you decide the next change. Then:

| Verdict `kind` | What it means | Your next turn |
|---|---|---|
| `passed` + `ORACLE_PASSED` | prediction held, criterion's oracle is green | move to the next red criterion (predict again) |
| `failed` | oracle still red | the invariant was wrong OR the change was wrong - one corrective change, re-predicted |
| `mismatch` (`PREDICTION_MISMATCH`) | oracle moved, but not as predicted | your model of the code is wrong - gather a fact before changing again |
| `noop` | oracle state unchanged | your change had no effect - do not repeat it; find why |
| `regression` (`REGRESSION`) | a previously-green criterion went red | fix the regression first; it outranks new work |
| any + `STATE_REVISITED` | you are looping (same change/state seen before) | STOP. A different change or a fact-gathering turn - never the same edit again |

`progress_delta` reflects ONLY contract-oracle state (+1 when a criterion flips
red->green, -1 on regression, 0 otherwise). A `passed` prediction is a **fact about your
prediction**, not proof you are closer to done - only `progress_delta > 0` is that. Do
not confuse "I was right about what would happen" with "the feature advanced."

## The Turn Record (log every turn)

Emit a compact turn record each turn so the loop can audit your decisions later. Each
record is appended as one line to `.episteme/turn-record.jsonl`. Keep
it small - it is a log line, not an artifact. Shape (see
`templates/turn-record.json`):

```json
{
  "turn": 14,
  "feature": "contract-auth",
  "criterion": "AC-3",
  "belief": "verifyToken() currently ignores the exp claim; callers expect a throw on expiry",
  "hypothesis_id": "led-0008",
  "next_change": "add exp-claim check in verifyToken(), throw TokenExpiredError",
  "prediction": "auth.spec.ts::rejects-expired-token red->green; suite 41/41; 0 type errors",
  "expected_invariant": "expired JWT -> 401 body {error:'token_expired'}",
  "confidence": 0.7,
  "deviated_from_policy": false,
  "deviation_reason": null
}
```

Field rules:
- `hypothesis_id` references a ledger entry (`led-XXXX`) when the change tests/rests on
  one; `null` if it is a self-contained criterion.
- `confidence` is your own estimate the prediction holds (0-1). Low confidence on an
  `assumed`-backed change is correct and honest - it flags a probe, not a failure.
- `deviated_from_policy: true` REQUIRES a `deviation_reason`. Silent deviation is the
  thing the critic will catch.
- After the verdict returns, the loop pairs this record with the verdict; you do not
  write the verdict here (that is the verifier's output).

## Rationalization Table

| Excuse | Reality |
|---|---|
| "These two fixes are related, I'll do both this turn" | Then a red verdict can't tell you which broke it. One change. Split it. |
| "It's obviously correct, no need to predict the oracle" | "Obvious" code fails oracles constantly. If it's obvious, the prediction takes 10 seconds. Write it. |
| "I can't predict the outcome, but let me just try it" | Inability to predict = a missing fact. Gather the fact; don't gamble a turn. |
| "The policy said to do X, so X must be right" | Policy is advisory. The last verdict outranks it. Deviate and record why. |
| "I'll just claim it's done, the test usually passes" | "Usually" is not an oracle run. No completion claim without a fresh verdict. |
| "The ledger says auth uses argon2, so I'll build on that" (entry is `assumed`) | `assumed` ≠ `verified`. Either verify it first or make your change a low-confidence probe. |
| "Same change failed last turn but maybe this time" | `STATE_REVISITED`. Repeating an edit is a loop. Change the change or gather a fact. |
| "I'll predict loosely - 'it should work'" | Unfalsifiable invariant. The verifier can't check it. Demote to explore or make it concrete. |
| "While I'm in this file I'll tidy it up" | Scope drift. The critic reads the contract and will reject it. Refactor in its own predicted turn. |
| "The prediction was right, so we're closer to done" | Prediction-held is a fact about you, not progress. Only the oracle flipping green is progress. |

## Red Flags - STOP and Restart the Turn

- About to edit code without having written `prediction` + `expected_invariant`
- About to change more than one behavior in a turn
- About to claim a criterion is satisfied without a verdict in hand
- About to re-plan without having read the last verdict
- Your invariant contains "should", "correctly", "properly", "works", "handles it"
- You are repeating an edit the verdict already returned `noop`/`failed`/`STATE_REVISITED` on
- You are building on a ledger entry tagged `assumed` as if it were `verified`
- You can't say what the oracle will show - and you're about to type code anyway

All of these mean: stop, fix the input or the prediction, restart the turn.

## Worked Example (bugfix criterion)

**Contract AC-3:** "An expired token is rejected with 401 `{error:'token_expired'}`."
Paired oracle: `pnpm test auth.spec.ts::rejects-expired-token`.

**READ** - last verdict (turn 13) was `passed` for AC-2 (valid token accepted). Ledger
`led-0008` (`assumed`): "verifyToken ignores exp claim." Policy
`recommended_next_action`: "implement expiry rejection in verifyToken."

**PREDICT**
- `prediction`: "auth.spec.ts::rejects-expired-token red->green; full suite 41/41; 0 type errors."
- `expected_invariant`: "decode().exp < now -> throw TokenExpiredError -> handler maps to 401 body {error:'token_expired'}."
- `confidence`: 0.75 (depends on `led-0008`, which is `assumed` - this turn verifies it).

**CHANGE** - add the exp-claim check in `verifyToken()` and the error->401 mapping. Nothing else.

**HAND OFF** - invoke `verifying-against-contract`. It runs the oracle.

**OBSERVE** - verdict returns `passed`, `ORACLE_PASSED`, `progress_delta: +1`.
The criterion's oracle flipped red->green: real progress. The `assumed` `led-0008` is now
backed by an observation - hand that to the curator to flip it to `verified`. Next turn:
the next red criterion.

Had it returned `mismatch` (e.g. token rejected but body was `{error:'invalid'}`), the
model was wrong about the error mapping - gather the fact (read the error handler) before
the next change, do not re-guess.

## Hand-off Checklist (before ending the turn)

- [ ] Read the contract criterion in play, the policy's `recommended_next_action`, the ledger, AND the last verdict
- [ ] Wrote a concrete, falsifiable `prediction` (named oracle + observable transition)
- [ ] Wrote a concrete `expected_invariant` (a checkable assertion, no "should/correctly")
- [ ] Made exactly ONE change toward this one criterion - no scope drift
- [ ] Did NOT claim the criterion satisfied on my own word
- [ ] Handed to `verifying-against-contract` to run the cheap oracle
- [ ] Logged the turn record (incl. `deviation_reason` if I deviated from policy)
- [ ] Will read the returned verdict in full before planning the next change

Can't check every box? You broke the Iron Law. Revert to the last green oracle state and
restart the turn.
