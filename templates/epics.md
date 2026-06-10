---
prd: .episteme/prd.md                  # source artifact: the functional requirements
architecture: .episteme/architecture.md # source artifact: decisions + confidence tiers
status: draft                          # draft | approved
---

<!--
  Produced by episteme:sharding-into-stories from .episteme/prd.md + .episteme/architecture.md.
  The epistemic spine of this document is TRACEABILITY:
    - every PRD functional requirement maps to >=1 story (no requirement dropped),
    - every story names the FRs it realizes,
    - the FR Coverage Map is the checkable closure proof (the cheap oracle of this phase),
    - a story resting on an `uncertain`/`assumed` architecture decision carries a Risk: flag
      (and a spike story precedes it where the uncertainty is load-bearing).
  Each story below is later handed to episteme:writing-a-story (one story id -> full story + contract).
  Lineage: adapts BMAD bmad-create-epics-and-stories (FR inventory -> epic -> story + coverage map).
-->

# <project / feature name> - Epic & Story Breakdown

One or two sentences: what this breakdown decomposes and from which PRD scope.

## Requirements Inventory

<!--
  Transcribe FRs VERBATIM from the PRD, keeping the PRD's own ids (FR1, FR-AUTH-2, ...).
  Do NOT renumber and do NOT invent requirements. If an FR is vague/missing, send it back
  to the PRD skill - do not paper over it here.
-->

### Functional Requirements
- `FR1`: <one-line statement, verbatim from the PRD>
- `FR2`: <...>
- `FR3`: <...>

### Non-Functional Requirements
- `NFR1`: <...>

### UX / Additional Requirements
- <...>

## Epic List

<!--
  Organize by USER VALUE, not technical layers. Each epic stands alone (Epic 2 must not
  require Epic 3 to function). Prefer fewer/larger epics when the design is settled;
  split only at a real risk boundary. Consolidate epics that churn the same core files.
  Every epic lists the FRs it covers.
-->

### Epic 1: <user-centric title>
<goal: what the user can do after this epic>
**FRs covered:** FR1, FR2

### Epic 2: <user-centric title>
<goal>
**FRs covered:** FR3, FR7

<!-- ...one block per epic... -->

## Epics & Stories

<!--
  Per epic, list its stories IN DEPENDENCY ORDER (a story may rest only on EARLIER stories,
  never a later one). Each story is a THIN VERTICAL SLICE, sized so its per-story loop
  (contract -> policy -> implement <-> verify -> critic -> curate) is tractable in one focused pass.
  Story ids are FLAT and sequential across the whole document (story-01, story-02, ...),
  regardless of which epic groups them; the `epic:` field records the grouping. That flat
  `story-NN` id is the canonical one used in the FR coverage map, in `Realizes:` references,
  in the story filename (`.episteme/stories/story-NN.md`), and in the contract's `stories: [...]`.
  Each story carries:
    epic:            the epic id it belongs to (e.g. Epic 1).
    Realizes:        the FR ids it realizes (>=1; or, for a spike, the FRs it unblocks).
    Risk: (optional) names an `uncertain`/`assumed` architecture decision it depends on.
    Acceptance sketch: one line of what "done" looks like (NOT the full Given/When/Then -
                       that is episteme:writing-a-story's job).
  Sizing: >~3 FRs, or an acceptance sketch needing "and" more than once -> probably two stories.
-->

### Epic 1: <title>

#### story-01: <thin-slice title>
epic: Epic 1
Realizes: FR1
Acceptance sketch: <one observable behavior that defines done>

#### story-02: <thin-slice title>
epic: Epic 1
Realizes: FR2
Acceptance sketch: <...>

### Epic 2: <title>

<!-- A spike story FIRST when a load-bearing architecture uncertainty must be resolved
     before a dependent story can be specified. Its job: probe/decide, produce a
     `verified` ledger finding, unblock the dependents. -->
#### story-03 [spike]: <resolve the uncertainty>
epic: Epic 2
Realizes: (unblocks FR7)
Acceptance sketch: <the decision/finding produced, recorded as a verified ledger entry>

#### story-04: <thin-slice title>
epic: Epic 2
Realizes: FR7
Risk: carries "<architecture decision>" (architecture: uncertain - <why>)
Acceptance sketch: <...>

## FR Coverage Map

<!--
  One row PER FR (go FR-by-FR through the inventory, not story-by-story, so a missed FR
  cannot hide). "Realized by" must list >=1 story. Story `Realizes:` lines and this map
  MUST agree. Then write the explicit closure verdict.
-->

| FR   | Realized by              | Notes |
|------|--------------------------|-------|
| FR1  | story-01                 | <brief> |
| FR2  | story-01, story-02       | split across two slices |
| FR3  | story-...                | |
| FR7  | story-04 (story-03 spike first) | risk: uncertain token store |

**Closure verdict:** `Coverage: <N> FRs, all mapped` - OR - list any FR with an empty
"Realized by" cell as a GAP (the breakdown then FAILS the Iron Law and must not hand off).
Also confirm: no orphan stories (every story realizes >=1 FR or is a spike tied to FRs),
and every story's `Realizes:` line is consistent with the rows above.
