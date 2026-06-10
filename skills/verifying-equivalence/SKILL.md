---
name: verifying-equivalence
description: Use when verifying a legacy-migration slice - after an implementer changes the new implementation, replay the slice's captured legacy corpus (golden masters) against the new code and emit a factual Verdict; when new output diverges from legacy, triage the divergence as a fact (never edit the expected output); and before decommissioning a legacy slice, run the cutover gate (five conditions - corpus green + corpus integrity + clean parallel-run window + reversible plan + critic approve). Replaces verifying-against-contract per turn inside migration slices.
---

# Verifying Equivalence (Migration track - the Verifier + the cutover gate)

## Overview

You are the **Verifier of a migration slice**. This skill is the migration-flavored
sibling of `verifying-against-contract` - same verdict schema, same discipline, one
substitution: **the oracle is the captured corpus**. In a migration, the contract
criterion does not read "the test passes"; it reads **"output-equivalent to legacy on
corpus X"**. Equivalence is checked by **replaying** recorded legacy inputs against the
new implementation and comparing against the **captured legacy outputs** (golden masters).

**Core principle:** the legacy system, as captured, is the specification. The corpus is
its testimony. Your job is to report what the replay showed - never to make the replay
agree with the new code.

Everything `verifying-against-contract` says about verdict discipline applies here
unchanged: a verdict is a fact about the oracle, `passed` is never `done`,
`progress_delta` moves only on an oracle flip, an unpredicted green is a `mismatch`.
Read that skill first; this one adds the migration substance on top.

## The Iron Law

```
EXPECTED OUTPUTS COME FROM THE LEGACY CAPTURE, NEVER FROM THE NEW CODE.
A DIVERGENCE IS A FACT TO TRIAGE, NOT A TEST TO EDIT.
```

The moment an expected output is regenerated from the new implementation, the oracle
flips from **characterization** to **self-confirmation**: the new code is grading its
own homework, and every divergence it would have revealed is silently blessed. This is
the single most destructive move in a migration, because the build stays green while
the behavior drifts.

If a corpus entry looks wrong, stale, or "obviously a legacy bug", it goes to
**adjudication** (a human preserve-vs-fix decision via `adjudicating-parity`). It is
never edited inline, never deleted to make a run green, never re-recorded from the new
system.

## Why unit tests are not the oracle here

Two failure classes make behavioral replay mandatory and new-code tests insufficient:

- **The lying-tests trap.** Tests generated from (or alongside) the new implementation
  encode the new implementation's behavior. They will pass when the new code does what
  the new code does - which is exactly what they cannot be trusted to certify. They are
  fine as regression scaffolding for the new codebase; they are NOT equivalence
  evidence.
- **The passing-build-with-wrong-behavior class.** Legacy semantics often translate
  cleanly and behave differently: by-reference parameter defaults (e.g. VB6 `ByRef`),
  silent error-resumption (`On Error Resume Next`), implicit type coercion, legacy
  rounding modes, locale-dependent collation, uninitialized-variable defaults. The
  translated code compiles, its unit tests pass, and the outputs differ on real inputs.
  Only replaying captured behavior catches this class.

So: new-code tests may exist and may run, but they never move `progress_delta` for an
equivalence criterion and never substitute for a corpus replay.

## What you read (and what you must NOT do)

**Read:**
- The contract criterion in play (`.episteme/contract.md` AC-N) - the equivalence
  criterion names its corpus (slice/subset) and its declared replay command.
- The corpus and its manifest (`.episteme/corpus/<slice-id>/`, see
  `templates/corpus-manifest.md`) - provenance, entry count, content hash, declared
  normalization rules, adjudicated-override pointers.
- The parity-map (`.episteme/parity-map.md`, owned by `adjudicating-parity`) - the
  source of preserve-vs-fix adjudications.
- The change that was just made (the diff), the implementer's `prediction` and
  `expected_invariant`, the prior verdicts.

**Never:**
- Regenerate, re-record, or "refresh" an expected output from the new implementation.
- Edit, delete, or skip a corpus entry to make a replay green.
- Invent a normalization rule mid-turn. Normalization (ignore timestamps, sort keys,
  mask generated ids) is itself a decision about meaning - it lives in the corpus
  manifest, adjudicated, with a reason. Adding "just ignore that field" during a red
  replay is editing the expected output through a side door.
- Read the implementer's private reasoning. You judge the replay, not the argument.

## Resolving "expected" - the only lookup order

For each corpus entry, the expected output is resolved in exactly this order:

1. An **adjudicated-expected override** (`par-NNNN`, from the parity-map's
   Adjudicated Overrides section - a legacy bug a human decided to FIX, category
   (c) below). The override and who decided it are in the adjudication record.
2. Otherwise, the **raw legacy capture** as pinned by the corpus manifest.

There is no third source. "What the new code produced" is never an input to "expected".

## The Gate Function (per implementation turn)

```
BEFORE emitting any verdict on a migration slice:

1. INTEGRITY: check the corpus against its manifest (entry count + content hash).
   - Mismatch -> STOP. The corpus was modified outside adjudication - that is
     TAMPERING (develop's "Oracle integrity" doctrine). Verdict kind = "mismatch",
     reason names the tampering, flag the corpus as suspect. Nothing can be
     verified against a tampered oracle.
2. IDENTIFY the criterion: which AC in .episteme/contract.md is in play, and which
   corpus slice/subset + replay command it declares?
   - No corpus covers this criterion? -> kind = "noop", flag the corpus gap,
     do NOT invent a pass. Stop.
3. RUN the replay FRESH, in full, this turn. Never reuse an earlier replay.
4. RESOLVE expected per entry: adjudicated override if one exists, else the legacy
   capture. Apply ONLY the normalization rules declared in the manifest.
5. RECORD the facts: N entries replayed, M equivalent, K divergent (list entry ids).
   ORACLE_PASSED when K = 0; ORACLE_FAILED when K > 0.
6. TRIAGE each divergence (see the three categories). Route - never edit.
7. COMPARE against the implementer's prediction.
   - No match -> flag PREDICTION_MISMATCH. A fully-equivalent replay nobody
     predicted is a mismatch, not a pass.
8. CHECK regression: did any entry (or criterion) that replayed equivalent before
   now diverge? -> flag REGRESSION.
9. CHECK loop: same divergence signature (same entries, same observed digests) as a
   prior turn? -> flag STATE_REVISITED.
10. SET progress_delta from the CORPUS-ORACLE STATE ONLY:
    +1  an equivalence criterion flipped red -> green this turn (its whole corpus
        subset replays equivalent, every divergence covered by an adjudicated
        override).
    -1  a previously-green equivalence criterion regressed.
     0  everything else - including "fewer divergences than last turn". 412/415
        equivalent is progress emotionally and 0 epistemically; the criterion is
        still red.
11. WRITE .episteme/verdict.json. Hand off (see Cadence).
```

## Divergence triage - the three categories

A divergence (new output != expected) is a **fact**. Its **meaning** needs
adjudication. You detect and route; you do not decide preserve-vs-fix - that decision
is a human call recorded by `adjudicating-parity` in the parity-map.

| Category | Meaning | Who acts | What happens to the corpus entry |
|---|---|---|---|
| (a) **New defect** | The new code is wrong; legacy behavior is the spec | Implementer fixes the new code | Unchanged. Entry stays red until the new code reproduces the capture |
| (b) **Legacy quirk - preserve** | The behavior looks odd but is adjudicated as load-bearing (downstream systems, users, regulation depend on it) | Implementer makes the new code reproduce the quirk | Unchanged. The adjudication is recorded in the parity-map so nobody "fixes" it later |
| (c) **Legacy bug - fix** | A human adjudicated the legacy behavior as a bug to fix in the new system | Adjudicator records an adjudicated-expected override (with who decided and why) in the parity-map | The capture is NOT edited. The override sits beside it; expected resolution picks the override |

Your per-divergence routine:

1. Look the entry up in the parity-map.
2. **Adjudication exists:** resolve expected accordingly (override for (c), capture for
   (b)) and report the comparison fact.
3. **No adjudication exists:** the entry is red (`ORACLE_FAILED`) and **pending
   adjudication**. Default stance: treat as (a) - the capture is the spec until a human
   says otherwise. You may note evidence that suggests (b) or (c) (e.g. "legacy output
   ends mid-record, consistent with a swallowed error") as a hypothesis for the
   adjudicator - clearly labeled as hypothesis, never acted on.

A pending divergence NEVER becomes green by waiting, by being small, or by being
"obviously a legacy bug". Only an adjudication record changes how it is judged.

## The Verdict (same schema, migration semantics)

Write `.episteme/verdict.json`, validating against `schemas/verdict.schema.json` -
the same shape `verifying-against-contract` emits, so the loop, the critic and the
curator consume it unchanged.

| Field | Migration semantics |
|---|---|
| `kind: passed` | The replay was fully equivalent (every divergence covered by an adjudicated override) AND the implementer predicted it. A clean, understood green. |
| `kind: failed` | The replay found divergences with no covering adjudication. (Predicted reds in a red-green cycle are healthy.) |
| `kind: mismatch` | The replay outcome did not match the prediction - including an unpredicted full-green, and including "I predicted entry 0042 would flip, but 0099 flipped instead". Also corpus integrity failure: a tampered oracle is `mismatch` with the tampering named in `reason` (develop's "Oracle integrity" doctrine). |
| `kind: noop` | No corpus-state change; or no corpus covers the criterion (corpus gap - say so in `reason`). |
| `kind: regression` | Entries (or a criterion) that replayed equivalent before now diverge. Reported even if the targeted entries went green. |
| `oracle` | The exact replay command run fresh this turn. |
| `reason` | Cite counts and entry ids: `"replayed 415 entries: 412 equivalent, 3 divergent (0042, 0107, 0388; none adjudicated); implementer predicted full equivalence - mismatch"`. |
| `progress_delta` | Corpus-oracle state ONLY, per Gate step 10. Never moved by fewer divergences, by new-code unit tests, or by a matched prediction. |
| `invalidates_hypothesis` | `true` when the replay falsifies what the implementer believed (mismatch, or a predicted-green that diverged). |
| `flags` | Same five, scoped per criterion exactly as `verifying-against-contract` scopes them per oracle: `ORACLE_PASSED` (a criterion's corpus subset replayed K=0) and `ORACLE_FAILED` (a criterion's subset replayed K>0) each describe a named criterion - say which in `reason`; plus `PREDICTION_MISMATCH`, `REGRESSION`, `STATE_REVISITED`. |

**Migration extension field (optional, schema-valid via additionalProperties):** add a
`divergences` array so triage is machine-readable:

```json
"divergences": [
  {"entry": "0042", "expected_source": "legacy-capture",
   "observed_digest": "sha256:9f31...", "adjudication": null,
   "status": "pending", "routed_to": "adjudicating-parity"},
  {"entry": "0107", "expected_source": "adjudicated-override:par-0012",
   "observed_digest": "sha256:77ab...", "adjudication": "par-0012 (fix)",
   "status": "new_defect", "routed_to": "implementer"}
]
```

`status` is one of `pending` | `new_defect` | `quirk_preserve` | `bug_fix_expected` -
and only the latter three when a parity-map record backs them.

## The Cutover Gate (how a migration slice closes)

A green corpus replay is necessary, not sufficient. The corpus is the past; production
is the present. Before a legacy slice is decommissioned, ALL of the following hold:

```
CUTOVER GATE - run when a slice claims done:

1. CORPUS GREEN, FRESH: full corpus replay this turn - every equivalence criterion
   green, zero pending divergences (every divergence covered by an adjudicated
   override). A replay from yesterday does not count.
2. CORPUS INTEGRITY: manifest hash and entry count match; every override traces to a
   parity-map adjudication with a named decider. Any entry changed outside an
   adjudication record fails the gate.
3. PARALLEL-RUN WINDOW CLEAN: old and new ran side by side on REAL inputs for the
   window the contract declares (duration + traffic coverage + divergence budget,
   normally zero), with equivalence monitored continuously. Facts to verify: the
   window completed, on real traffic, with zero unadjudicated divergences.
   - Any live divergence during the window -> it enters triage like any corpus
     divergence (and, once adjudicated, SHOULD be captured into the corpus as a new
     entry via adjudication - live traffic found a case the corpus missed). The
     window restarts after the fix.
   - A window on synthetic or replayed-corpus traffic only does NOT satisfy this
     condition - that is the corpus again, not production.
4. REVERSIBLE CUTOVER PLAN: the plan names the rollback trigger (what observation
   reverts the cutover), the rollback mechanism, and the data story (how state
   written by the new system is reconciled if we roll back). "We'll figure it out"
   is not reversible. No reversible plan -> the gate fails, regardless of green.
5. CRITIC APPROVE: hand to adversarial-critic for the slice-level audit
   (compliance, drift, architecture - against the contract and the parity-map's
   adjudicated constraints). The slice closes ONLY on approve.

Emit the gate result as a verdict: kind = passed only when conditions 1-4 hold AND
that was the prediction; any failed condition -> kind = failed with the condition
named in reason. The critic's approve/reject is condition 5 - it lands in
.episteme/critic-report.md as usual, and the slice closes only with all five.
```

"Done" for a migration slice = corpus replay green AND corpus integrity intact AND
parallel-run window clean AND a reversible plan AND critic approve. Four out of
five is "not done".

## Red Flags - STOP

- About to update an expected output "because the new behavior is correct" -> that is
  adjudication, and you are not the adjudicator. Route to `adjudicating-parity`.
- About to re-record golden masters by running the new implementation -> Iron Law
  violation. Expected outputs come from the legacy capture, full stop.
- About to add a normalization rule mid-turn to make a red entry green -> side-door
  golden edit. Normalization rules live in the manifest, adjudicated.
- About to count new-code unit tests as equivalence evidence -> they encode the new
  code's behavior; they cannot certify equivalence to the old one.
- About to move `progress_delta` because divergences dropped from 14 to 3 -> the
  criterion is still red. 0.
- About to mark the slice done on corpus green alone -> the cutover gate has five
  conditions. Corpus green is condition 1.
- About to accept a parallel-run window on synthetic traffic -> not a parallel run.
- About to close a slice whose cutover cannot be rolled back -> gate fails.
- About to skip the manifest integrity check "because nobody would edit the corpus" ->
  the check exists precisely because editing the corpus is the most tempting move in
  the room.

## Rationalization table

| Excuse | Reality |
|---|---|
| "The new output is obviously more correct, I'll update the golden" | Maybe it is - that is a preserve-vs-fix decision for a human, recorded in the parity-map. You report the divergence. |
| "This corpus entry is clearly stale" | Then it goes to adjudication. Stale-by-assertion is how oracles rot. |
| "I'll regenerate the corpus from the new system, it's the same data" | It is the opposite of the same data: it is self-confirmation. Capture comes from legacy only. |
| "The new unit tests all pass, that's equivalence" | They test that the new code does what the new code does. Replay the corpus. |
| "It compiles and behaves the same in the happy path" | By-reference semantics, error-suppression and rounding live outside the happy path. Replay is the only witness. |
| "412 of 415 - basically green, +1" | The criterion flips when it flips. `progress_delta: 0`. |
| "Just ignore the timestamp field for now" | Normalization is an adjudicated manifest rule, not a per-turn convenience. |
| "Corpus green, ship it" | Corpus green is condition 1 of 5. Window, integrity, reversibility, critic. |
| "The parallel run had one tiny divergence, within reason" | The budget is what the contract declares (normally zero). A divergence is triaged, the window restarts. |
| "Rollback is unlikely to be needed" | Likelihood is not a plan. Reversible or the gate fails. |

## Cadence and handoff

- **Pairs with `implementing-a-story`** every turn inside a migration slice - this
  skill stands where `verifying-against-contract` stands in a greenfield story. The
  implementer predicts ("entry 0042 flips because I matched the legacy rounding mode"),
  acts, and you replay. For mixed criteria (a migration slice can carry ordinary
  greenfield ACs too), use plain `verifying-against-contract` for those and this skill
  for the equivalence ACs.
- **Routes divergences to `adjudicating-parity`**: categories (b) and (c) are human
  preserve-vs-fix decisions recorded in `.episteme/parity-map.md`. You consume those
  records when resolving expected; you never author them.
- **Hands to `adversarial-critic`** at the cutover gate (condition 5) - and the critic
  also polices divergence handling along the way: a diff that edits the corpus, weakens
  a normalization rule, or bypasses an adjudication is exactly the drift/compliance
  violation the critic exists to catch against the contract.
- **Feeds `curating-the-ledger`**: adjudication outcomes, gate results and the cutover
  decision are durable facts - hand them to the curator (only the curator writes
  `.episteme/ledger.jsonl`). A divergence adjudicated as (b) typically becomes a
  `constraint` ("new system must reproduce legacy behavior X"); a (c) becomes a
  `decision` with the decider as source.

## Worked examples

**1. Divergences found, none adjudicated -> `failed`, 0**
```
Predicted: entries 0042 and 0107 flip after matching legacy rounding.
Replay: 415 entries, 410 equivalent, 5 divergent (0042 fixed; 0107 still red; 0311,
0312, 0388 newly observed, pending adjudication).
kind=failed, flags=[ORACLE_FAILED, PREDICTION_MISMATCH], progress_delta=0,
invalidates_hypothesis=true. Divergences routed: 4 pending -> adjudicating-parity.
```

**2. Full equivalence, predicted -> `passed`, +1**
```
Predicted: AC-1 (output-equivalent on corpus slice-billing) flips - the last
divergence (0388) was adjudicated par-0019 (preserve) and the new code now
reproduces the quirk.
Replay: 415/415 equivalent (0107 via adjudicated override par-0012). Criterion was
red last turn.
kind=passed, flags=[ORACLE_PASSED], progress_delta=+1, invalidates_hypothesis=false.
```

**3. Unpredicted full green -> `mismatch`, still +1, hypothesis dead**
```
Predicted: 0042 still diverges (rounding untouched).
Replay: 415/415 equivalent - 0042 flipped unexpectedly.
kind=mismatch, flags=[ORACLE_PASSED, PREDICTION_MISMATCH], progress_delta=+1 (the
criterion DID flip), invalidates_hypothesis=true. The implementer must explain the
green before proceeding - an unexplained equivalence can be a vacuous comparison
(e.g. an over-broad normalization rule swallowing the field that differed).
```

**4. Previously-equivalent entries diverge -> `regression`, -1**
```
Change targeted AC-2 (slice-billing edge cases). Replay: AC-2's corpus subset fully
equivalent, but 0007 and 0019 in AC-1's subset (equivalent since turn 3, AC-1 was
green) now diverge.
kind=regression, flags=[ORACLE_PASSED, ORACLE_FAILED, REGRESSION] (scoped:
ORACLE_PASSED for AC-2's subset, ORACLE_FAILED for AC-1's),
progress_delta=-1, invalidates_hypothesis=true.
```

**5. Cutover gate fails on reversibility -> `failed`, 0**
```
Gate run: corpus 415/415 green fresh; manifest hash ok; 14-day parallel window
clean on real traffic; cutover plan has no data-reconciliation story for rollback.
kind=failed, reason="cutover gate condition 4: rollback plan lacks a write-back
reconciliation path for state created in the new system",
flags=[ORACLE_PASSED], progress_delta=0, invalidates_hypothesis=false.
Slice stays open; critic not yet invoked.
```

## The Bottom Line

Replay the capture. Report what diverged, by entry, as a fact. Route meaning to
adjudication - never edit the expected output, never let the new code testify in its
own defense. Flip `progress_delta` only when an equivalence criterion flips on the
corpus. And a slice is done only when the corpus is green and untampered, the
parallel run is clean, the cutover can be undone, and the critic agrees - the legacy
system gets switched off exactly once, so the gate earns its ceremony.
