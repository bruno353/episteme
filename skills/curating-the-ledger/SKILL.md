---
name: curating-the-ledger
description: Use when recording a decision/constraint/finding/assumption to durable memory, after any verdict, or at a feature/story boundary - appends typed entries to .episteme/ledger.jsonl with source + authority and runs ledger-check before the ledger is considered updated. The sole owner of the ledger; never laundering an assumption into a fact.
---

# Curating the Ledger (Voice 4 - the Curator)

## Overview

The ledger is the project's memory. It is a typed, append-only log of every
durable decision, constraint, observed fact, and open assumption - each tagged
with **where it came from** (`source`) and **how much we trust it** (`authority`).
It survives handoffs, fresh subagents, and context compaction. For a human
reviewer it doubles as the audit trail of what was decided and why.

You are the **sole owner** of `.episteme/ledger.jsonl`. No other voice writes to
it. Your discipline is what keeps Pillar 2 (curated memory) and Pillar 3
(fact/hypothesis separation) honest.

**Core principle:** A hypothesis stays `assumed` until an oracle flips it to
`verified`. The curator never launders an assumption into a fact.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO LEDGER UPDATE WITHOUT A CLEAN ledger-check RUN

After writing entries:
    python3 tools/ledger-check.py .episteme/ledger.jsonl
Exit 0 = updated. Exit != 0 = NOT updated. Fix every problem and re-run.
```

If you have not seen `OK: N entries valid` in this message, the ledger is not
updated and you may not claim it is. This is the same gate as
verification-before-completion, applied to memory: evidence before the claim.

## When to Use

- **After every verdict** - the verifier confirmed or invalidated a hypothesis.
  Flip the affected `assumed` entry to a new `verified` one (via `supersedes`),
  or record the new finding.
- **At a feature/story boundary** - consolidate: carry forward what still holds,
  amend what changed, retire what was disproven.
- **When the contract changes** - write a `contract_version` entry pointing at
  the new snapshot.
- **When the critic rejects with `items_to_revisit`** - actually reconsider
  those entries against the cited evidence, do not just re-assert them.

Recording one entry mid-task is fine and cheap. The heavier consolidation pass
happens at boundaries.

## The Schema (the only shape that counts)

Every line in `.episteme/ledger.jsonl` is one JSON object validated against
`schemas/ledger.schema.json`. Required fields on **every** entry:

| Field | What it is |
|---|---|
| `id` | `led-` + >=4 digits, e.g. `led-0007`. Unique, never reused. |
| `type` | `decision` \| `constraint` \| `finding` \| `assumption` \| `contract_version` |
| `statement` | The decision/fact/rule in one sentence. |
| `source` | Where it came from: `grep src/users`, `contract AC-4`, `verdict turn 9`, `story-12 brainstorm`. |
| `authority` | `verified` (an oracle/observation backs it) or `assumed` (inferred). |
| `created_at_turn` | The loop turn index now (freshness). |

Optional but load-bearing:

- `oracle_ref` - the exact command/test backing a `verified` entry.
- `evidence_for` / `evidence_against` - cited evidence, kept side by side.
- `supersedes` - the `led-` id this entry amends (must already exist earlier in the file).
- `feature`, `tags` - scoping/filtering.

**The schema's one hard rule:** a `verified` entry MUST carry either a non-empty
`oracle_ref` OR at least one `evidence_for` item. There is no verification
without cited evidence - the validator rejects it.

When choosing a `type`: `decision` = a choice you made; `constraint` = a rule
that must hold; `finding` = an observed fact about the codebase; `assumption` =
an unverified inference; `contract_version` = a pointer recorded when
`contract.md` changed.

## The Curator's Discipline (the doctrine that transfers)

These are distilled from the wmv2 Knowledge Curator. They are non-negotiable.

1. **One observation is not a rule.** Promote an entry to `authority: verified`
   only when an oracle backs it or evidence repeats. A single glance, a single
   green test on a happy path, a "looks right" - that is `assumed`. Cite the
   oracle in `oracle_ref`, or the repeated evidence in `evidence_for`.
2. **Assumed stays assumed until an oracle flips it.** You do not get to upgrade
   a hypothesis to a fact because the task needs it to be true. The oracle
   decides; you record. (This is the Iron Law in memory form.)
3. **Carry forward, do not re-derive.** Prior entries that the new evidence does
   not contradict stay in force - you simply do not touch them. Stability over
   novelty. Re-litigating settled facts every pass is churn, not curation.
4. **Amend, never overwrite.** A line is append-only. When a belief changes,
   write a NEW entry with a NEW id and set `supersedes` to the old id. The old
   line stays in the file as history. Never edit or delete a past line.
5. **Never fabricate or invert a finding.** Record only what the source actually
   showed. Do not flip a direction, soften a failure into a success, or invent a
   detail the observation did not contain. If you renamed or reinterpreted
   something, keep the original source label visible and mark the inference.
6. **Source + authority on EVERY entry.** No anonymous memory. If you cannot name
   a source, you do not have a ledger entry yet - you have a thought.
7. **Keep competing interpretations alive.** When the evidence supports more than
   one reading, do NOT collapse to the convenient one. Write each plausible entry
   `assumed`, list `evidence_for` / `evidence_against`, and let the next verdict
   discriminate. Premature certainty is the failure you are guarding against.
8. **Track failed ideas with WHY and what would reopen them.** A disproven idea
   is memory, not garbage. Record it (e.g. an `assumption` with `evidence_against`
   citing the verdict that killed it) and state plainly what new evidence would
   make it worth reconsidering. This stops the loop from re-trying dead ends.
9. **Current facts outrank old summaries.** When a fresh `verified` finding
   conflicts with an older entry, the fresh one wins - record it and `supersedes`
   the stale one. Freshness (`created_at_turn`) is part of authority.

## The Procedure

```
1. READ the existing ledger end to end (it is your prior memory).
2. For each thing to record:
   a. Pick the type and write a one-sentence statement.
   b. Name the source. No source -> not an entry yet.
   c. Set authority: verified ONLY with an oracle_ref or repeated evidence_for;
      otherwise assumed.
   d. If it changes an earlier belief, set supersedes to that id (amend, not edit).
3. APPEND the new line(s) to .episteme/ledger.jsonl (never rewrite old lines).
4. RUN the integrity gate:
       python3 tools/ledger-check.py .episteme/ledger.jsonl
5. If exit != 0: fix EVERY reported problem, re-run, repeat until exit 0.
6. ONLY THEN report the ledger as updated.
```

ids must be strictly increasing and unique - scan the file for the highest
existing `led-NNNN` and increment. `supersedes` may only point at an id that
already appears on an **earlier** line.

## Good Entries (these pass `ledger-check`)

A finding backed by a real oracle (`verified`, with `oracle_ref`):
```json
{"id":"led-0002","type":"finding","statement":"existing UserService already hashes passwords with argon2id","source":"grep -rn 'argon2' src/users","authority":"verified","oracle_ref":"grep -rn 'argon2' src/users","created_at_turn":4,"feature":"contract-auth","tags":["reuse"]}
```

A constraint that came from the contract but is not yet enforced (`assumed`):
```json
{"id":"led-0003","type":"constraint","statement":"the POST /auth/refresh endpoint must be rate-limited (contract AC-4 forbids unbounded refresh)","source":"contract-auth AC-4","authority":"assumed","created_at_turn":4,"feature":"contract-auth","tags":["security"]}
```

A decision recorded as a hypothesis before any oracle exists (`assumed`):
```json
{"id":"led-0001","type":"decision","statement":"auth uses short-lived JWT + refresh tokens, not server-side sessions","source":"story-12 brainstorm","authority":"assumed","created_at_turn":3,"feature":"contract-auth","tags":["architecture"]}
```

Amending that decision AFTER a verdict made it real - note `supersedes` +
`evidence_for`, and the old line is left untouched in the file:
```json
{"id":"led-0005","type":"decision","statement":"auth uses short-lived JWT (15m) + rotating refresh tokens (7d), refresh persisted in Redis with a denylist on rotation","source":"verdict turn 9 + ADR-2","authority":"verified","oracle_ref":"npm test -- auth.spec.ts","created_at_turn":10,"supersedes":"led-0001","evidence_for":["led-0004 verified","ADR-2"],"feature":"contract-auth","tags":["architecture"]}
```

The full set above lives in `templates/ledger.example.jsonl` and passes:
`OK: 5 entries valid`.

## Bad Entries (these FAIL `ledger-check` - and why)

A `verified` entry with no `oracle_ref` and no `evidence_for` - the cardinal sin,
an assumption laundered into a fact:
```json
{"id":"led-0007","type":"finding","statement":"the rate limiter blocks the 6th refresh within 60s","source":"my reading of the middleware","authority":"verified","created_at_turn":11}
```
```
L1: schema [<root>] ... is not valid under any of the given schemas
```
Fix: either run the test and cite it in `oracle_ref`, or mark it `assumed`.

A missing required field (`created_at_turn`):
```json
{"id":"led-0008","type":"decision","statement":"use Redis for the denylist","source":"chat","authority":"assumed"}
```
```
L2: schema [<root>] 'created_at_turn' is a required property
```

A reused id:
```
L3: duplicate id 'led-0007' (first seen L1)
```
Fix: never reuse an id; increment from the highest in the file.

A `supersedes` pointing at an id that does not exist earlier (or at all):
```json
{"id":"led-0009","type":"finding","statement":"...","source":"x","authority":"assumed","created_at_turn":12,"supersedes":"led-0042"}
```
```
L4: 'led-0009' supersedes unknown id 'led-0042'
```
Fix: amend only entries that already exist on an earlier line.

## Red Flags - STOP

- Marking an entry `verified` because you are confident, not because an oracle ran.
- Editing or deleting a past line instead of appending a `supersedes` entry.
- Claiming the ledger is updated without a fresh `OK:` from `ledger-check`.
- Collapsing two live interpretations into one to "keep it clean."
- Dropping a failed idea entirely instead of recording why it failed.
- Re-asserting an entry the critic flagged in `items_to_revisit` without
  reconsidering it.
- An entry with no `source` ("I just know this is how it works").

## Rationalization Table

| Excuse | Reality |
|---|---|
| "It's obviously true, mark it verified" | Obvious != oracle-backed. No `oracle_ref`/`evidence_for` -> `assumed`. |
| "The old line is wrong, I'll just fix it" | Append-only. Write a new entry with `supersedes`; history stays. |
| "ledger-check will probably pass" | Run it. "Probably" is not exit code 0. |
| "Two readings is messy, pick one" | Premature collapse is the bug. Keep both `assumed` with evidence. |
| "That idea failed, delete it" | Failed ideas are memory. Record why + the reopen condition. |
| "The task needs this to be a fact" | Need does not promote authority. The oracle does. |
| "No clear source, but it's right" | No source = not an entry. Go find the source first. |

## Why This Matters

Without source + authority, memory rots into confident fiction: an assumption
written once gets read later as settled fact, a stale decision outlives the
evidence that changed it, a dead end gets re-tried because nobody recorded why
it died. The authority tag and the `supersedes` chain are what let a fresh
subagent - or a human auditor six weeks later - tell "we verified this" from "we
guessed this," and see exactly when and why a belief changed. The `ledger-check`
gate is the cheap deterministic oracle (Pillar 4) that makes that promise
enforceable instead of aspirational.

## The Bottom Line

```
Write the entry -> name the source -> set authority honestly ->
append (never overwrite) -> run ledger-check -> see OK -> THEN it's recorded.
```

Skip the gate, and the ledger is just unverified text.
