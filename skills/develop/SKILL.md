---
name: develop
description: Use when starting any non-trivial coding feature, bugfix, or legacy migration and you want it built right - runs Episteme's epistemic loop so "done" is proven against a contract, not declared. Tracks: Micro (trivial change), Quick (straight to the loop), Full (brief -> PRD -> architecture -> stories), Migration (excavate -> adjudicate parity -> slices, equivalence-verified).
---

# Develop - the Episteme orchestrator

## Overview

The happy-path orchestrator. It runs the epistemic loop end to end by invoking the
voice skills in order and keeping their artifacts coherent in `.episteme/`. Each
voice is also a standalone skill; `develop` is what you use when you want the whole
disciplined flow. It offers four graduated tracks (see below); Quick, Full and
Migration share the same per-story loop.

**Core principle:** "done" is proven against a contract by a cheap oracle and an
independent critic, never declared by the implementer.

## The `.episteme/` working directory (canonical layout)

Single source of truth for where artifacts live - every voice agrees on it.

**Per-story loop (both tracks):**

| File | Owner voice | What it is |
|---|---|---|
| `.episteme/contract.md` | writing-the-contract | the verifiable spec; each AC paired with its oracle |
| `.episteme/policy.json` | synthesizing-the-policy | the gated plan (readiness + reachability + retrospective) |
| `.episteme/verdict.json` | verifying-against-contract | the latest turn's factual verdict |
| `.episteme/critic-report.md` | adversarial-critic | the post-diff audit against the contract |
| `.episteme/ledger.jsonl` | curating-the-ledger | typed curated memory (authority + freshness) |
| `.episteme/turn-record.jsonl` | implementing-a-story | append-only log of implement turns |

**Full-track planning artifacts (greenfield/large only):**

| File | Owner voice | What it is |
|---|---|---|
| `.episteme/brief.md` | writing-a-brief | problem / users / goals / non-goals; seeds the ledger |
| `.episteme/prd.md` | writing-a-prd | vision + FRs with testable (oracle-shaped) consequences |
| `.episteme/architecture.md` | deciding-architecture | append-only decisions with confidence tiers (the Theorist voice) |
| `.episteme/epics.md` | sharding-into-stories | FR inventory -> epics -> stories + an FR coverage map |
| `.episteme/stories/<story-id>.md` | writing-a-story | one ready-for-dev story (flat id `story-NN`) |

**Migration-track artifacts (legacy rewrites only):**

| File | Owner voice | What it is |
|---|---|---|
| `.episteme/behavior-inventory.md` | excavating-behavior | the capability map exhumed from the legacy system; every row authority-tagged |
| `.episteme/captures/<CAP-id>/` | excavating-behavior | raw golden masters per capability (recorded inputs/outputs, snapshots, replay recipes) |
| `.episteme/parity-map.md` | adjudicating-parity | per-capability decisions (retire/retain/as-is/fix/repurchase) + quirk adjudications + slice plan |
| `.episteme/corpus/<slice-id>/` | writing-the-contract (assembled at slice-contract time) | the slice's replay corpus + manifest (content-hashed; the equivalence oracle) |

Create `.episteme/` (and the subdirs you need) at the start if missing.

## The Iron Law

```
NO "DONE" WITHOUT ALL THREE:
  1. every contract acceptance criterion's oracle is GREEN (verifier), and
  2. adversarial-critic returned `approve` against the contract + ledger, and
  3. ledger-check ran clean on .episteme/ledger.jsonl (curator).
Miss any one and the feature is NOT done - say so plainly.
```
(Spike stories and the Micro track are the exceptions - their gates are a verified
ledger finding + clean ledger-check, and the existing suite green + a curated
finding, respectively.)

## Tracks (graduated - use the lightest one that fits)

- **Micro track** (a trivial change: typo, rename, config bump, one-line fix with an
  obvious existing oracle): predict -> make the one change -> run the existing suite ->
  curate one ledger finding. No contract file, no policy, no critic. If the suite
  shows ANY unexpected behavior change, escalate to Quick. Micro is for changes where
  an oracle already exists and no new behavior is intended - it is NOT a loophole for
  feature work.
- **Quick track** (default; mini-apps, internal tools, a single feature): skip
  planning, go straight to the per-story loop on one `contract.md`.
- **Full track** (greenfield, large features, multiple stories): run the planning
  phases first, then run the per-story loop once per story.
- **Migration track** (legacy rewrites, e.g. a VB6 app to a modern web stack): the
  code precedes the intent - excavate behavior first, then adjudicate, then migrate
  slice by slice with equivalence oracles. See "Migration track" below.

Choose the lightest track that fits; ceremony that does not buy verification is waste.

## Full track - planning phases (run once, before any code)

Each phase invokes a lifecycle skill, writes its artifact, and curates the ledger
as it goes (assumptions -> `assumed` entries, established facts -> `verified`).
Set each artifact's `status` forward as its phase completes.

```
A. DISCOVERY     -> writing-a-brief        -> .episteme/brief.md     (seeds ledger)
B. SPEC          -> writing-a-prd          -> .episteme/prd.md       (FRs w/ testable consequences; [ASSUMPTION] -> ledger)
C. ARCHITECTURE  -> deciding-architecture  -> .episteme/architecture.md  (confidence tiers; decisions/constraints -> ledger)
D. STORIES       -> sharding-into-stories  -> .episteme/epics.md     (FR coverage map: every FR -> >=1 story)
                 -> writing-a-story (per story) -> .episteme/stories/<story-id>.md
E. PER STORY     -> writing-the-contract (story ACs -> contract w/ oracles) -> THE LOOP (below)
```

Order stories so spikes and dependencies come first. Then run the loop for each
story in turn; the ledger and architecture carry context across stories.

## Migration track - phases (legacy rewrites; the code IS the intent)

Greenfield assumes intent precedes code; migration inverts it. Do NOT write a brief
or PRD for a migration - excavate and adjudicate instead:

```
M-A. EXCAVATE     -> excavating-behavior    -> .episteme/behavior-inventory.md + captures/
                     (capture from the RUNNING system = verified; read-from-code = assumed)
M-B. ADJUDICATE   -> adjudicating-parity    -> .episteme/parity-map.md
                     (parity is the null hypothesis: retire/retain/as-is/fix/repurchase
                      per capability; every quirk gets a HUMAN preserve-or-fix decision)
M-C. ARCHITECTURE -> deciding-architecture  -> .episteme/architecture.md (brownfield:
                     the target stack + the seams; confidence tiers as usual)
M-D. SLICES       -> sharding-into-stories  -> .episteme/epics.md (input = the parity
                     map's value-stream slices, not PRD FRs; strangler-fig order,
                     capture-first spikes before slices that rest on `assumed` behavior)
M-E. PER SLICE    -> writing-the-contract (criteria = "output-equivalent to legacy on
                     the captured corpus"; the oracle IS the corpus replay - captured
                     from legacy, blind to the new code) -> THE LOOP, with
                     verifying-equivalence in place of verifying-against-contract ->
                     cutover gate (corpus green + corpus integrity + clean parallel-run
                     window + reversible cutover + critic approve - five conditions) ->
                     decommission the slice.
```

The blindness direction flips in migration: greenfield authors oracles blind to the
implementation; migration captures oracles from the legacy system, blind to the NEW
implementation. Expected outputs NEVER come from the new code. Authoring the slice
contract ASSEMBLES the corpus: the relevant `.episteme/captures/<CAP-id>/` entries
are composed into `.episteme/corpus/<slice-id>/` with a content-hashed manifest; from
then on the corpus is read-only (verifying-equivalence checks the hash).

## Contract renegotiation (two-way, cheap by design)

When implementation falsifies a contract assumption - an AC is wrong, unreachable as
written, or the design underneath it was disproven - do NOT grind against the gate
and do NOT silently edit the contract:

1. Invoke `writing-the-contract` in AMEND mode: bump `version`, change ONLY the
   affected criterion, re-author its oracle (blind, watch it fail again).
2. The curator records a `contract_version` entry citing what was falsified and by
   which verdict/finding.
3. The critic treats an amended contract as the new truth; it flags only UNRECORDED
   drift (work that diverges from the contract with no amendment trail).

Amending one criterion is a small step, not a restart. A gate you cannot cheaply
renegotiate gets bypassed in practice - this path exists so the gate stays honest.

## Oracle integrity (anti-tamper)

- Oracle/test files authored for the contract are IMMUTABLE to the implementer. If
  an oracle seems wrong, that is a contract renegotiation (above), never an edit.
- The verifier checks oracle files are unchanged since authoring (diff against the
  contract version) before trusting a green run; an edited oracle, a monkeypatched
  exit, or a skipped test is TAMPERING -> verdict `mismatch` + the event goes to the
  ledger and the critic.
- In the Migration track, the corpus manifest's content hash is this same check for
  golden masters.

## The per-story loop

Maintain a `turn` counter starting at 0; pass it as `created_at_turn` to the
curator and `turn_index` to verdicts. Announce each voice as you invoke it.

```
0. SETUP: ensure .episteme/ exists. Read .episteme/ledger.jsonl (prior memory).

1. CONTRACT  -> writing-the-contract
   .episteme/contract.md: each AC paired to a cheap oracle, authored BLIND to any
   implementation and confirmed RED first. Curator records a `contract_version` entry.

2. POLICY    -> synthesizing-the-policy
   Reads contract + ledger. .episteme/policy.json with a readiness status. If
   `not_ready`/`probe_more`: act on its discriminators (gather facts, curate
   findings) and re-synthesize. Do NOT implement off a `not_ready` policy.

3. BUILD LOOP (repeat until every contract oracle is green):
   a. implementing-a-story  -> ONE code change + a prediction (append .episteme/turn-record.jsonl).
   b. verifying-against-contract -> run the oracle, write .episteme/verdict.json.
   c. curating-the-ledger   -> record the finding; flip `assumed`->`verified` only when an
      oracle backed it; run ledger-check.
   d. read the verdict BEFORE the next change. On mismatch/failed, re-plan from the
      verdict (never guess); if the policy's assumptions were invalidated, re-synthesize.

4. CRITIC    -> when all criteria green, adversarial-critic
   Reads contract + ledger + the diff (never the implementer's reasoning). Writes
   .episteme/critic-report.md.
   - approve -> close.
   - reject  -> route items_to_revisit to the curator and step 3. Anti-deadlock: after
     2 consecutive same-signature rejections, force-approve with a logged caveat
     (record it in the ledger and surface it to the human).

5. CLOSE -> Iron Law satisfied. Final curation pass + report: what shipped, the green
   oracles, the critic verdict, open caveats. (Full track: move to the next story.)
```

## Spike stories

A `[spike]` story (from sharding-into-stories) resolves an uncertainty; its "done"
is NOT a passing test. For a spike, skip the contract/policy/critic gates and instead:
run the investigation, then `curating-the-ledger` records the targeted finding -
`verified` if an oracle/observation backed it, honestly `assumed` if still open - and
`ledger-check` runs clean. The spike's cheap oracle IS the ledger gate. Run spikes
before the stories that depend on them, so dependents start from a `verified` finding.

## Loop control rules

- One change per build turn; never batch. The verifier runs after every change.
- `progress_delta` moves only when a contract oracle flips red->green (+1) or
  green->red (-1). Several turns at `progress_delta: 0` -> stop and re-synthesize the
  policy (the approach may be unreachable - see the policy's reachability audit).
- Never skip the contract "because it's simple" on feature work. A one-criterion
  contract is still the contract. (Trivial no-new-behavior changes belong to the
  Micro track, which leans on the EXISTING suite as its oracle.)
- The curator is the only writer of `.episteme/ledger.jsonl`; everyone else reads it.

## Red flags - STOP

- Implementing before a contract with oracles exists (non-spike).
- Starting the build loop off a `not_ready` policy.
- Claiming "done" without the critic's `approve` and a clean ledger-check.
- Editing beyond what the active criterion needs (the critic will flag drift).
- Treating an `assumed` ledger entry as if it were `verified`.
- Running the Full track for a one-file mini-app (use Quick), or Quick for a typo (use Micro).
- The implementer editing an oracle/test file instead of renegotiating the contract.
- Writing a brief/PRD for a legacy migration (use the Migration track - excavate, don't invent intent).

## Standalone use

Invoke a single voice directly when you don't need the whole loop - e.g.
`adversarial-critic` to audit an existing diff against a contract, or
`curating-the-ledger` to record a decision. The loop is the default for building a
feature; the voices are the tools.
