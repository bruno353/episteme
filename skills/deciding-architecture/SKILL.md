---
name: deciding-architecture
description: Use after a PRD exists and before sharding into stories - whenever you need to decide and record system architecture (components, interfaces, data, tech choices) as durable, append-only decisions instead of a vibe in someone's head. Builds .episteme/architecture.md step by step, tags every claim with a confidence tier, prefers silence over speculation, revises rather than overwrites, and curates each decision into the ledger as a decision/constraint entry the adversarial critic later enforces.
---

# Deciding Architecture (Full track, phase 3 - solutioning; carries the Theorist voice)

## Overview

`.episteme/architecture.md` is the slowly-evolving structural model of the
system: its components, their interfaces, the data, and the technology choices -
each recorded as a durable decision, not a passing opinion. It is built
**incrementally and append-only** from `.episteme/prd.md`, one decision category
at a time, and it is the source the later phases (`sharding-into-stories`,
`writing-the-contract`, `adversarial-critic`) read to keep implementation
coherent.

This skill **carries the Theorist voice** of the Episteme loop (wmv2's
`world_model_theorist`): the slow, conservative model of structure that downstream
voices trust as authoritative. Because they trust it, a confident wrong claim here
cascades. So this skill's whole job is to be *honest about how much it knows*.

**Core principle:** an architecture decision is a *claim about structure*. Every
claim carries a **confidence tier**, an architecture you are unsure of is recorded
as **unknown** rather than invented, and a decision is **revised by superseding
it, never silently overwritten**. Each decision becomes a typed ledger entry -
`verified` only when a spike/test/prior-art backs it, `assumed` when it is a bet.

**Violating the letter of these rules is violating the spirit of these rules.**

This is phase 3 of the Full track. It reads `.episteme/prd.md` (produced by
`writing-a-prd`) and hands off to `sharding-into-stories`. Lineage: the
append-only, step-driven document and `stepsCompleted` frontmatter are adapted
from BMAD's `bmad-create-architecture` (MIT) - credited, adapted; the Theorist
doctrine and the ledger-curation discipline are Episteme's.

## The Iron Law

```
NO ARCHITECTURE DECISION WITHOUT A CONFIDENCE TIER AND A LEDGER ENTRY.

Every recorded decision/constraint MUST state its tier
  (uncertain | tentative | confirmed)
and be curated into .episteme/ledger.jsonl as a `decision` or `constraint`
entry whose authority matches the tier:
  confirmed (spike/test/prior-art backs it) -> authority: verified (cite the oracle)
  uncertain / tentative (a bet)             -> authority: assumed
A "confirmed/verified" claim with no cited oracle is the cardinal sin - it is a
guess laundered into a fact. Mark it assumed, or go run the spike.
```

If you cannot name the tier and append the ledger entry, you have an opinion, not
an architecture decision. Do not write it into the document as settled.

## The Theorist doctrine (the differentiator - non-negotiable)

These three rules are distilled from the wmv2 World Model Theorist and adapted
from grids to codebase/domain structure. They are why this skill exists.

### 1. Confidence tiers on every claim

Tag every architectural claim - tech choice, component boundary, data shape,
interface - with how much evidence stands behind it:

| Tier | Earned when | Ledger authority |
|---|---|---|
| `uncertain` | 1 data point (one doc line, one "I think", a single example) | `assumed` |
| `tentative` | 2 independent, consistent data points | `assumed` |
| `confirmed` | a spike/PoC ran, a test/benchmark backs it, OR strong prior art in *this* codebase | `verified` (cite the oracle) |

A vendor's marketing page is not a data point. Your preference is not a data
point. "Confirmed" requires that you (or this codebase already) *did the thing and
observed the result*. When in doubt, drop a tier.

### 2. Silence over speculation

If you do not know, write **`unknown`** - do not invent a clean answer to fill the
section. An honest gap drives a spike later; a fabricated decision drives a wrong
build that nobody questions because it "looks decided". Record the open question
in the document's `## Open questions` and (when it blocks work) as an
`assumption` ledger entry with the evidence that would resolve it.

> Adding noise is worse than admitting ignorance. The downstream consumers read
> this document as authoritative - a wrong claim with high confidence causes
> cascading failures.

### 3. Revise, never overwrite

The document is **append-only**. When a later decision changes an earlier one, you
do **not** edit the old line. You **supersede** it: append a new decision that
references the old one's id, states the new choice, and says *why it changed*
(what new evidence moved it). The old decision stays visible as history. The same
move happens in the ledger via `supersedes`. Promote a tier (uncertain ->
tentative -> confirmed) the same way - by superseding, citing the new evidence.

## When to Use

- After `.episteme/prd.md` exists and before `sharding-into-stories` (Full track,
  phase 3).
- When you are about to make - or have already made informally - structural
  choices (database, framework, service boundaries, API style, auth model, data
  model) that multiple stories will depend on.
- To resume an in-progress architecture: read the existing
  `.episteme/architecture.md`, look at `stepsCompleted`, and continue from the
  next uncompleted step (see *Resuming*).

**When NOT to use:** the Quick track (mini-apps, single feature) skips
architecture entirely - go straight from the contract to the loop. Do not invent
heavy architecture for a one-file change.

## The `.episteme/` files this skill touches

| File | Role here |
|---|---|
| `.episteme/prd.md` | **read** - the source of truth this architecture serves (FRs, glossary, assumptions) |
| `.episteme/architecture.md` | **write (append-only)** - the decision document you build |
| `.episteme/ledger.jsonl` | **write via `curating-the-ledger`** - each decision/constraint as a typed entry |

Create `.episteme/architecture.md` from `templates/architecture.md` if it does not
exist. Never write the ledger by hand - invoke `curating-the-ledger`, which owns
it and runs `ledger-check`.

## The steps (append-only, step-driven; `stepsCompleted` in frontmatter)

The document is built one section at a time. After each step's content is
appended, update the `stepsCompleted` array in the frontmatter, then move on. This
makes the work resumable and the document a faithful trail of how the architecture
was decided. **Do not look ahead** - each step appends only its own section.

```
0. INIT      -> read .episteme/prd.md fully; create architecture.md from template
                if absent (else resume from stepsCompleted). Record which PRD/
                version you read.
1. CONTEXT   -> restate, from the PRD, the forces architecture must serve:
                the FRs, the non-functional constraints, the [ASSUMPTION]s,
                the glossary terms. No decisions yet - just the inputs, each
                with a confidence tier (a PRD assumption is `uncertain`).
2. DECISIONS -> the core choices, by category (data, auth/security, API,
                frontend, infra). For EACH: state the choice, the tier, the
                evidence, what it affects, and alternatives considered. Then
                curate it into the ledger (decision/constraint). UNKNOWN where
                you don't know.
3. CONSTRAINTS -> the rules that must hold across the build ("all DB access
                goes through the repository layer", "no module imports across
                feature boundaries"). These become `constraint` ledger entries -
                they are what the adversarial-critic enforces against the diff.
4. STRUCTURE -> components and their boundaries; map PRD FRs/epics to where they
                live; the interfaces between components. Tier each boundary.
5. RISKS+OPEN -> the open questions (silence-over-speculation made explicit), the
                spikes that would resolve them, and the known risks. Each open
                question that blocks work becomes an `assumption` ledger entry.
6. COMPLETE  -> integrity pass + handoff to sharding-into-stories.
```

### Step 0 - Init / resume

- Read `.episteme/prd.md` **fully** (all FRs, the assumptions index, the
  glossary). If there is no PRD, stop: "Architecture needs a PRD. Run
  `writing-a-prd` first." Architecture decisions made without the PRD's forces are
  guesses. **Migration track exception:** there is no PRD - read
  `.episteme/parity-map.md` + `.episteme/behavior-inventory.md` as the forces
  source (capabilities to migrate, coupling facts, slice plan) and proceed.
- If `.episteme/architecture.md` does not exist, copy `templates/architecture.md`
  to it. Fill `prd_source` (which PRD/version) and `date`.
- If it **does** exist with `stepsCompleted`, you are resuming: read the whole
  document, identify the highest completed step, and continue from the next one.
  Do not re-run completed steps; do not rewrite their sections.
- Maintain a `turn` counter (start at the PRD's last turn, or 0) to pass to the
  curator as `created_at_turn`.

### Step 1 - Context from the PRD

Append `## 1. Context (from the PRD)`. List, sourced from `.episteme/prd.md`:
the functional requirements architecture must satisfy; the non-functional forces
(scale, latency, compliance, team constraints); the PRD's `[ASSUMPTION]`s that bear
on structure; the glossary terms you will use precisely. **Tier each line** - a PRD
assumption arrives as `uncertain`. No decisions here, only the inputs. This is the
folded fact-gathering step; nothing is `verified` yet because nothing has been
spiked.

### Step 2 - Core architectural decisions

Append `## 2. Core decisions`. Work category by category (data, auth/security,
API/communication, frontend if applicable, infra/deployment). For each decision
use the **decision block** (see *The decision block* below). Critically:

- If you genuinely do not know yet, write the choice as `UNKNOWN` with the open
  question - do **not** invent a clean answer. (Silence over speculation.)
- Set the tier honestly. A choice you merely prefer is `uncertain`. A choice the
  PRD + one prior project agree on is `tentative`. A choice a spike or this
  codebase's existing pattern proves is `confirmed`.
- Verify technology *facts* before claiming them confirmed (current stable
  version, that a library actually supports X). A claim about the world is
  `verified` only if you checked; otherwise `assumed`.
- After writing each decision block, **curate it into the ledger** via
  `curating-the-ledger`: a `decision` entry, `authority` matching the tier, the
  evidence in `evidence_for`. Get the `led-NNNN` id back and write it into the
  decision block's `Ledger:` line.

### Step 3 - Constraints (what the critic will enforce)

Append `## 3. Constraints`. A constraint is a rule that must hold across the whole
build - e.g. "all DB access goes through the repository layer", "domain layer
never imports from the web layer", "every external call has a timeout". These are
the most load-bearing entries in the whole document because the
`adversarial-critic` reads them and **rejects diffs that violate them**. Each
constraint:

- is stated as a checkable rule (not a vibe - "be clean" is not a constraint;
  "no SQL strings outside `src/db/`" is);
- carries a tier and the evidence;
- is curated into the ledger as a `constraint` entry.

A constraint backed only by preference is `assumed`. One backed by a measured
failure ("we tried direct access and got N+1 queries - spike #2") is `verified`,
cite the spike.

### Step 4 - Components & structure

Append `## 4. Components & structure`. Name the components/modules/services and
their responsibilities; draw the boundaries between them; list the interfaces
(public functions, endpoints, types, events) each exposes; and **map the PRD's FRs
/ epics to where they live** (FR-3 -> `src/billing/`). Tier each boundary - a
boundary you are inventing fresh is `uncertain`; one mirroring an existing,
working module in this codebase is `confirmed` (cite it). Interfaces named here are
what `writing-the-contract` will turn into oracle surfaces later.

### Step 5 - Risks & open questions

Append `## 5. Risks & open questions`. This is silence-over-speculation made into a
deliverable. List every `unknown` you left above, the **spike** that would resolve
each (the cheapest experiment that turns `uncertain`/`tentative` into `confirmed`),
and the known risks of the bets you took. Each open question that *blocks* a story
becomes an `assumption` ledger entry stating what evidence would resolve it - so
the build loop knows what to probe, not guess.

### Step 6 - Complete & hand off

- **Integrity pass:** re-read the whole document. Check that every decision has a
  tier and a `Ledger:` id; that no section silently overwrote an earlier one (only
  supersedes); that every `UNKNOWN` appears in `## 5`. Confirm the last
  `curating-the-ledger` run printed `OK: N entries valid`.
- Set frontmatter `stepsCompleted: [0,1,2,3,4,5,6]`, `status: complete`.
- **Hand off to `sharding-into-stories`**, which reads this document to slice the
  build into stories that reference the components and constraints recorded here.

## The decision block (use this shape in steps 2-4)

```markdown
### D-<n>: <the decision, one line>
- **Choice:** <what was chosen - or `UNKNOWN` with the open question>
- **Tier:** uncertain | tentative | confirmed
- **Evidence:** <the data points / spike / prior art - name them; a spike id if `confirmed`>
- **Affects:** <FRs / components this constrains, e.g. FR-3, billing component>
- **Alternatives considered:** <what you rejected and why (one line each)>
- **Ledger:** led-NNNN          <!-- filled after curating-the-ledger -->
```

When a later decision changes D-3, do not edit D-3. Append D-9 with
`- **Supersedes:** D-3 - <why it changed (new evidence)>` and supersede the ledger
entry too.

## Curating each decision into the ledger

After each decision/constraint, invoke `curating-the-ledger`. The mapping is fixed:

| Document tier | Ledger `type` | Ledger `authority` | Must carry |
|---|---|---|---|
| confirmed | decision / constraint | `verified` | `oracle_ref` (the spike/test/benchmark) OR an `evidence_for` item |
| tentative | decision / constraint | `assumed` | `evidence_for` listing the 2 data points |
| uncertain | decision / constraint | `assumed` | the single data point in `source` |
| open question that blocks work | assumption | `assumed` | what evidence would resolve it |

<Good>
A confirmed decision backed by a spike, curated as `verified`:
```
D-4: Use Postgres (not Mongo) for the billing store.
- Tier: confirmed
- Evidence: spike #1 - modelled invoices+line-items, ran the FR-3 reporting query;
  Postgres joins were 40ms vs a 3-collection aggregation in Mongo. Repo already
  runs Postgres for `users`.
- Affects: FR-3, billing component, data layer
- Alternatives considered: Mongo (rejected: relational reporting is core, spike #1)
- Ledger: led-0021
```
ledger entry: `type: decision`, `authority: verified`, `oracle_ref:` the spike, tier earned by an observed result.
</Good>

<Bad>
A preference dressed up as a confirmed fact:
```
D-4: Use Mongo - it's web-scale and flexible.
- Tier: confirmed
- Evidence: it's the modern choice.
- Ledger: led-0021 (authority: verified)
```
"Modern choice" is not a data point; no spike ran; `confirmed`/`verified` is a laundered guess. This is `uncertain`/`assumed` at best - and the unmeasured FR-3 reporting need probably makes it the wrong bet. Run the spike or mark it `uncertain`.
</Bad>

## Resuming an in-progress architecture

`stepsCompleted` is the resume marker. On re-entry: read the whole document, find
the highest number in `stepsCompleted`, continue from the next step. Never re-run
a completed step or rewrite its section - that would break append-only. If new
evidence changes a past decision, supersede it (a new block in the appropriate
section, plus a superseding ledger entry), do not edit the old one.

## Red Flags - STOP

- A decision with no confidence tier.
- A decision marked `confirmed` with no spike/test/prior-art cited (laundered fact).
- A section invented to "look decided" instead of an honest `UNKNOWN`.
- Editing or deleting an earlier decision instead of superseding it.
- Writing the ledger by hand instead of via `curating-the-ledger`.
- A "constraint" that is a vibe ("keep it clean") instead of a checkable rule.
- Starting architecture with no `.episteme/prd.md` (Full track) - or, on the
  Migration track, with no parity map + behavior inventory.
- Re-running a completed step / rewriting a section on resume.
- A tech-version or library-capability claim asserted without checking.

## Rationalization Table

| Excuse | Reality |
|---|---|
| "I'm confident, mark it confirmed" | Confidence is not evidence. `confirmed` needs a spike/test/prior art. Drop a tier or go run it. |
| "I'll fill this section in so it's not empty" | An invented decision is worse than `UNKNOWN` - nobody questions it and the wrong build ships. Silence over speculation. |
| "The old decision is wrong, I'll just fix the line" | Append-only. Supersede it with a new block + `Supersedes:`; the old line stays as history. |
| "It's obviously Postgres/React/whatever" | Obvious to you is `uncertain` until two data points or a spike. Tag it honestly. |
| "I'll record the ledger entries at the end" | Curate each as you go; the tier and the entry are one act. Batching invites laundering. |
| "Architecture doesn't need oracles, that's for the contract" | True - but `confirmed` still needs *cited evidence* (a spike result), and constraints still get enforced by the critic. |
| "The vendor docs say it scales, that's confirmed" | Marketing is not a data point. `confirmed` is what *you* observed in a spike or this codebase. |
| "We're in a hurry, skip the tiers" | The tier is one word. The cascading wrong build from an unmarked guess costs days. |

## Why This Matters

Architecture is the longest-lived memory in the project: stories, contracts, and
the critic all read it as settled truth. wmv2 learned the hard way that a slow
"world model" voice with no humility cascades - a confident wrong macro-claim
poisoned every downstream voice. The fix was confidence tiers, silence over
speculation, and revise-not-overwrite. Ported to code, those three rules let a
fresh subagent - or a human six weeks later - tell "we proved this with a spike"
from "we guessed this", see exactly when and why a decision changed, and trust the
constraints the critic enforces. The ledger linkage makes that promise auditable
instead of aspirational.

## The Bottom Line

```
Read the PRD -> for each structural choice: state it, tier it honestly,
cite the evidence (UNKNOWN if you don't have it) -> curate it into the ledger
(verified only with a spike, else assumed) -> supersede, never overwrite ->
update stepsCompleted -> hand off to sharding-into-stories.
```

An architecture decision with no tier is an opinion. A `confirmed` with no spike
is a guess in a fact's clothing. Tier it, back it, curate it - or say `unknown`.
