---
name: develop
description: Use when starting any non-trivial coding feature or bugfix and you want it built right - runs Episteme's epistemic loop so "done" is proven against a contract, not declared. Two tracks: Quick (straight to the loop) and Full (brief -> PRD -> architecture -> stories, then the loop per story).
---

# Develop - the Episteme orchestrator

## Overview

The happy-path orchestrator. It runs the epistemic loop end to end by invoking the
voice skills in order and keeping their artifacts coherent in `.episteme/`. Each
voice is also a standalone skill; `develop` is what you use when you want the whole
disciplined flow. It offers two tracks (see below) that share the same per-story loop.

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

Create `.episteme/` (and `.episteme/stories/`) at the start if missing.

## The Iron Law

```
NO "DONE" WITHOUT ALL THREE:
  1. every contract acceptance criterion's oracle is GREEN (verifier), and
  2. adversarial-critic returned `approve` against the contract + ledger, and
  3. ledger-check ran clean on .episteme/ledger.jsonl (curator).
Miss any one and the feature is NOT done - say so plainly.
```
(Spike stories are the one exception - see "Spike stories" below.)

## Tracks

- **Quick track** (default; mini-apps, internal tools, a single feature): skip
  planning, go straight to the per-story loop on one `contract.md`.
- **Full track** (greenfield, large features, multiple stories): run the planning
  phases first, then run the per-story loop once per story.

Choose Quick unless the work needs shared planning across several stories.

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
- Never skip the contract "because it's simple." A one-criterion contract is still the contract.
- The curator is the only writer of `.episteme/ledger.jsonl`; everyone else reads it.

## Red flags - STOP

- Implementing before a contract with oracles exists (non-spike).
- Starting the build loop off a `not_ready` policy.
- Claiming "done" without the critic's `approve` and a clean ledger-check.
- Editing beyond what the active criterion needs (the critic will flag drift).
- Treating an `assumed` ledger entry as if it were `verified`.
- Running the Full track for a one-file mini-app (use Quick).

## Standalone use

Invoke a single voice directly when you don't need the whole loop - e.g.
`adversarial-critic` to audit an existing diff against a contract, or
`curating-the-ledger` to record a decision. The loop is the default for building a
feature; the voices are the tools.
