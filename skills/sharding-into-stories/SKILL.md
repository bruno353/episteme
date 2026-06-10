---
name: sharding-into-stories
description: Use after a PRD and architecture exist and before any per-story work - turns .episteme/prd.md + .episteme/architecture.md into .episteme/epics.md - a functional-requirement inventory, an epic breakdown, a list of thin vertical-slice stories, and an FR coverage map that PROVES every functional requirement is realized by at least one story (no requirement dropped, each story tagged with the FRs it covers and any architectural uncertainty it carries)
---

# Sharding into Stories (Full track, phase 4)

## Overview

You read the planning artifacts - `.episteme/prd.md` and `.episteme/architecture.md` -
and you produce **one breakdown document**, `.episteme/epics.md`, that decomposes the
work into epics and into stories small enough that the per-story epistemic loop
(contract -> policy -> implement <-> verify -> critic -> curate) is tractable on each one.

**Core principle:** A story breakdown is only trustworthy if it is *checkable* -
every functional requirement in the PRD must be realized by at least one story, and
the FR coverage map is the artifact that proves it. A dropped requirement is the
silent bug of the planning phase, and the coverage map is its oracle.

**Violating the letter of this rule is violating the spirit of this rule.**

This is phase 4 of the Full track. You sit **after architecture, before
`writing-a-story`**. Each story you emit is later handed to `writing-a-story`, which
enriches one story id into a full story with its own `contract.md`. You produce the
breakdown that skill consumes.

Lineage: this adapts BMAD's `bmad-create-epics-and-stories` (MIT) - its FR inventory ->
epic -> story flow and its requirements coverage map. What Episteme threads through it
is the **traceability spine**: every story names the FRs it realizes, the coverage map
is a checkable closure proof, and stories that depend on `uncertain`/`assumed`
architecture are flagged as carrying that risk (and may need a spike story first). The
gerund-named, namespaced skill format follows Superpowers.

## When to Use

**Use when:**
- A `.episteme/prd.md` with enumerated functional requirements exists.
- A `.episteme/architecture.md` exists (you need its decisions and its confidence tiers).
- You are about to start building a Full-track feature and need to break it into
  loop-sized stories before any contract is written.

**Do NOT use to:**
- Write the PRD or invent requirements (that is the PRD skill - if the PRD is missing
  FRs, send it back; do not fabricate them here).
- Write a single story's full body or its contract (that is `writing-a-story` +
  `writing-the-contract`, per story).
- Build anything (that is `develop` running the loop on each story).
- Run the Quick track - that goes straight to `writing-the-contract`; there is no
  PRD/architecture to shard.

You produce a **plan**, not code and not contracts. You do not edit source files.

## The Iron Law

```
EVERY FUNCTIONAL REQUIREMENT IN THE PRD MAPS TO >=1 STORY,
AND EVERY STORY NAMES THE FRs IT REALIZES.

The FR coverage map is the proof. If any FR has zero stories, the
breakdown is INCOMPLETE - say so plainly and do not hand off.
```

An FR with no story is a requirement you silently agreed to drop. A story with no FRs
is scope you invented (or a missing trace). The coverage map makes both visible - it is
the cheap deterministic oracle of this phase (Pillar 4): a checkable closure proof, not
an opinion that "we covered everything."

## Inputs and output

**Read (do not skip any):**
1. `.episteme/prd.md` - the **functional requirements** (the things to cover), plus
   non-functional requirements, glossary, and any `[ASSUMPTION]` index. The FRs are
   your inventory. Use the PRD's own FR identifiers (`FR1`, `FR-AUTH-2`, etc.); do not
   renumber them.
2. `.episteme/architecture.md` - decisions and **confidence tiers**. Note every
   decision tagged `uncertain` / `assumed` / low-confidence - a story that depends on
   one inherits that risk and must be flagged.
3. `.episteme/ledger.jsonl` (if present) - prior curated memory; honor `authority` tags
   (`verified` vs `assumed`) when judging whether an architectural dependency is solid.

**Produce:** a single `.episteme/epics.md` (structure below; copy `templates/epics.md`).

## The procedure

Work through these in order. Each maps to a section of `.episteme/epics.md`.

### 1. Requirements inventory - extract, do not invent

Read the PRD and list **every** functional requirement verbatim (id + one-line
statement), then NFRs and any UX/additional requirements. This is a transcription, not a
synthesis: if the PRD does not state an FR, it does not exist here. If the PRD's FRs are
vague or missing, STOP and send it back to the PRD skill - a shaky inventory poisons the
whole map.

Cross-check each FR against `.episteme/architecture.md`: is there a decision that
realizes it? Note any FR the architecture is silent on, or covers only with an
`uncertain` decision - these will become risk-flagged stories or spikes.

### 2. Design the epic list - organize by user value

Group related FRs into epics. An epic is a **cohesive slice of user value**, not a
technical layer.

- ✅ "User Authentication & Profiles", "Content Creation", "Search & Discovery" - each
  delivers something a user can do, end to end.
- ❌ "Database Setup", "API Layer", "Frontend Components" - technical layers, no user
  value, and they force every later epic to wait on them.

Rules (from BMAD, kept because they earn their place):
- Each epic delivers complete functionality for its domain and **stands alone** - Epic 2
  must not require Epic 3 to function.
- Prefer **fewer, larger epics** when the design is settled and direction is unlikely to
  change. Split only at a genuine risk boundary or where early feedback could redirect
  later work.
- If several proposed epics keep modifying the same core files, that is churn -
  consolidate them into one epic with ordered stories.

For each epic record: title (user-centric), goal (what the user can do after it), and
the **FRs it covers**.

### 3. Shard each epic into thin vertical-slice stories

A story is a **thin vertical slice**: the smallest end-to-end increment that delivers a
piece of user-observable behavior and can run its own loop. "Thin vertical slice" means
it cuts through the layers it needs (UI -> logic -> data) for one behavior, rather than
building a whole horizontal layer.

Story ids are **flat and sequential** across the whole breakdown - `story-01`, `story-02`,
`story-03`, ... - regardless of which epic groups them. The epic grouping stays in the
`## Epic N:` headings (and each story records its `epic:`), but the canonical id used in
the filename (`.episteme/stories/<story-id>.md` with `<story-id>` = `story-NN`), in the FR
coverage map, in `Realizes:` references, and in the contract's `stories: [...]` is the flat
`story-NN`. A spike keeps the flat id too (e.g. `story-03 [spike]`).

Each story must:
- Be **loop-sized** - the per-story loop (write the contract + oracle, synthesize the
  policy, implement one change at a time, verify, critic, curate) is tractable for one
  developer/agent in one focused pass. If a story would need many contracts or a
  sprawling diff, split it.
- **Name the FRs it realizes** (`Realizes: FR2, FR3`). This is the traceability link the
  coverage map closes over. A story with no FR is either invented scope or a missing
  trace - resolve it.
- Have **no forward dependency** - it may build only on earlier stories, never on a
  later one. Order stories within an epic so each rests only on its predecessors.
- Carry a one-line **acceptance sketch** (what "done" will look like) - not the full
  Given/When/Then contract; that is `writing-a-story`'s job. Enough to size it and to
  let the contract author know the target.

Sizing heuristic: if a story realizes more than ~3 FRs, or its acceptance sketch needs
the word "and" more than once, it is probably two stories.

### 4. Flag architectural risk - and add spikes where needed

This is the epistemic flag the through-line demands. For each story, check the
architecture decisions it depends on:

- If it rests only on **settled** (high-confidence / `verified`) decisions -> no flag.
- If it depends on a decision the architecture marked **`uncertain` / `assumed` /
  low-confidence** -> set `Risk: carries <decision> (architecture: uncertain)` on the
  story. The downstream contract and policy will treat that dependency as `assumed`, not
  `verified`.
- If the uncertainty is load-bearing - the story genuinely **cannot** be specified until
  the unknown is resolved - insert a **spike story first**: a small story whose job is to
  resolve the uncertainty (probe, prototype, decide), produce a `verified` finding for
  the ledger, and unblock the dependent story. Order the spike before its dependents.

Do not launder an `uncertain` architecture decision into a confident story. The flag is
how the risk survives into the per-story loop, exactly as the curator keeps `assumed`
distinct from `verified`.

<Good>
```
### story-08: Reject expired session tokens
epic: Epic 2
Realizes: FR7
Risk: carries "token store = Redis with TTL" (architecture: uncertain - no load test yet)
Acceptance sketch: an expired token is rejected with 401 TOKEN_EXPIRED.
```
The dependency on an uncertain decision is named, so the contract/policy treat it as assumed.
</Good>

<Bad>
```
### story-08: Sessions
Acceptance sketch: sessions work.
```
No FRs named (breaks traceability), no risk flag despite resting on an unproven store, and
"sessions work" is not a sliceable behavior.
</Bad>

### 5. Build the FR coverage map - the closure proof

Produce a map with **one row per FR**, listing which story (or stories) realizes it. Go
FR-by-FR through the inventory from step 1 - not story-by-story - so a missed FR cannot
hide:

```
### FR Coverage Map
| FR   | Realized by        | Notes |
|------|--------------------|-------|
| FR1  | story-01           | login form + handler |
| FR2  | story-01, story-02 | split across register + verify |
| FR3  | story-05           | |
| FR7  | story-08 (story-07 spike first) | risk: uncertain token store |
| ...  | ...                | |
```

Then run the closure check explicitly and write the result:
- **Every FR has at least one story.** Any FR with an empty "Realized by" cell is a
  GAP - the breakdown fails the Iron Law. Add a story or send the FR back to the PRD if
  it is truly out of scope (and record that decision).
- **Every story's `Realizes:` line is consistent with the map** - if a story claims FR5
  but the map row for FR5 doesn't list it (or vice versa), the trace is broken; fix it.
- **No orphan stories** - every story realizes at least one FR (or is a spike explicitly
  tied to unblocking specific FRs).

State the verdict in the document: `Coverage: N FRs, all mapped` or list the gaps. This
line is the checkable artifact - the thing a reviewer can verify without rereading
the whole plan.

## Discipline (the gates, restated)

- **Closure or it's not done.** Every FR -> >=1 story; every story -> >=1 FR. The
  coverage map proves it FR-by-FR. (The Iron Law.)
- **Transcribe FRs, don't invent them.** Vague/missing FRs go back to the PRD; you do
  not paper over them with new requirements here.
- **Thin vertical slices, loop-sized.** Each story is small enough that its contract ->
  verify loop is tractable. When in doubt, split.
- **No forward dependencies.** Stories may rest only on earlier stories; order within an
  epic accordingly.
- **Uncertainty survives.** An `uncertain`/`assumed` architecture dependency becomes a
  `Risk:` flag on the dependent story (and a spike before it if it is load-bearing).
  Never silently treat it as settled.
- **Epics by user value, not layers.** And consolidate epics that churn the same files.
- **You are advisory.** You write the plan; `writing-a-story` enriches each story and
  `develop` builds it. You do not write contracts or code.

## Rationalization table

| Excuse | Reality |
|--------|---------|
| "These FRs are obviously all covered" | "Obviously" is not the map. Go FR-by-FR and write the row; a gap hides in exactly the FR you skipped. |
| "This FR is vague, I'll just write a reasonable story for it" | A story built on a vague FR inherits the vagueness. Send the FR back to the PRD; don't invent the requirement here. |
| "One big story is simpler than three" | If its loop isn't tractable in one focused pass it's too big. Thin vertical slices keep contract/verify honest. |
| "The architecture decision is probably fine, no need to flag it" | Probably ≠ verified. If the architecture tagged it uncertain, the story carries that risk - flag it or spike it. |
| "I'll let `writing-a-story` figure out the FR mapping" | Traceability is decided here, at the breakdown. The downstream skill enriches one story; it doesn't own the closure proof. |
| "An epic per technical layer is cleaner" | Layered epics deliver no user value and force every epic to wait on the others. Organize by what the user can do. |
| "This story is just setup, it doesn't realize an FR" | Then say which FRs it unblocks (a spike) - orphan stories are scope nobody asked for. |

## Red Flags - STOP

- An FR with an empty "Realized by" cell in the coverage map.
- A story with no `Realizes:` line (or one inconsistent with the map).
- A story whose acceptance sketch needs multiple "and"s, or that realizes 4+ FRs
  (probably too big - split it).
- A story that depends on a later story (forward dependency).
- A story resting on an `uncertain` architecture decision with no `Risk:` flag and no
  spike before it.
- Epics named after layers ("Database", "API", "Frontend") instead of user value.
- Inventing an FR the PRD never stated to make the map close.

**All of these mean: stop, fix the breakdown, and re-run the closure check before
handing off.**

## Output structure (.episteme/epics.md)

Copy `templates/epics.md`. Sections, in order:

1. **Requirements Inventory** - FRs (verbatim, with PRD ids), NFRs, UX/additional.
2. **Epic List** - each epic: title, goal, `FRs covered:`.
3. **Epics & Stories** - per epic (`## Epic N:` heading), its stories in dependency order;
   each story carries a flat sequential id (`story-NN`), an `epic:` field naming its epic,
   `Realizes:` (FR ids), optional `Risk:` flag, and a one-line acceptance sketch.
4. **FR Coverage Map** - one row per FR -> realizing story/stories + notes, then the
   explicit closure verdict (`Coverage: N FRs, all mapped` or the gap list).

Frontmatter carries `prd`, `architecture` (the source artifacts), and `status`
(`draft | approved`).

## Verification checklist

Before handing off to `writing-a-story`:

- [ ] Read `.episteme/prd.md` and `.episteme/architecture.md` this session (not from memory).
- [ ] Every PRD functional requirement is in the Requirements Inventory, verbatim, with
      its original id.
- [ ] Every epic is organized by user value and stands alone (no cross-epic forward
      dependency).
- [ ] Every story is a thin vertical slice, loop-sized, with no forward dependency.
- [ ] Every story has a `Realizes:` line naming >=1 FR (or is a spike tied to specific FRs).
- [ ] Every story depending on an `uncertain`/`assumed` architecture decision carries a
      `Risk:` flag, and a spike precedes it where the uncertainty is load-bearing.
- [ ] The FR coverage map has one row per FR; **no FR has an empty "Realized by" cell**.
- [ ] Story `Realizes:` lines and the coverage map agree (no broken traces, no orphans).
- [ ] The closure verdict is written explicitly in the document.

Can't check all boxes? The breakdown is not ready. Fix the gap; do not hand off.

## Handoff

Each story in `.episteme/epics.md` -> `writing-a-story` (takes one story id, enriches it
into a full story and authors its `.episteme/contract.md` with oracles). The contract
author treats every `Risk:`-flagged dependency as `assumed`, not `verified`. After each
story is enriched and built via `develop`, the curator records the realized FRs against
the coverage map - so the map doubles as a live progress/audit trail across the feature.

Re-run this skill when the PRD's FRs change (add/remove a requirement) or when the
architecture resolves an uncertainty (a spike may collapse, a `Risk:` flag may clear) -
re-derive the inventory and re-run the closure check.
