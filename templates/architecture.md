---
id: architecture                       # one per project
prd_source: .episteme/prd.md@v1        # which PRD/version this architecture serves
status: draft                          # draft | complete
stepsCompleted: []                     # [0,1,2,3,4,5,6] - append-only resume marker; never skip back
date: '<YYYY-MM-DD>'
---

<!--
  THE THEORIST VOICE (episteme:deciding-architecture). Build this document
  INCREMENTALLY and APPEND-ONLY, one section per step, updating stepsCompleted
  in the frontmatter after each.

  Three non-negotiable rules:
    1. CONFIDENCE TIERS - every decision is tagged uncertain | tentative | confirmed.
       confirmed requires a spike/test/prior-art you OBSERVED (not a preference).
    2. SILENCE OVER SPECULATION - write `UNKNOWN` rather than invent a clean answer.
       Honest gaps go in section 5 and drive spikes.
    3. REVISE, NEVER OVERWRITE - to change a past decision, APPEND a new block that
       Supersedes it and says why. Never edit/delete an earlier block.

  Every decision/constraint is curated into .episteme/ledger.jsonl via
  episteme:curating-the-ledger (confirmed -> verified+oracle; else assumed) and
  its led-NNNN id is written into the block's `Ledger:` line. Reads
  .episteme/prd.md; hands off to episteme:sharding-into-stories.

  Lineage: append-only step-driven document + stepsCompleted adapted from BMAD's
  bmad-create-architecture (MIT). Theorist doctrine + ledger curation are Episteme's.
-->

# Architecture Decision Document - <project name>

_Built collaboratively, section by section. Each decision carries a confidence tier
and is curated into the ledger. Gaps are recorded as `UNKNOWN`, not invented._

<!-- ============================================================ STEP 1 -->
## 1. Context (from the PRD)

<!-- The forces architecture must serve, sourced from .episteme/prd.md. No
     decisions yet. Tier each input - a PRD [ASSUMPTION] arrives as `uncertain`. -->

- **Functional requirements to satisfy:** <FR-1, FR-2, ... - one line each>
- **Non-functional forces:** <scale / latency / compliance / team / budget>
- **Inherited assumptions (from the PRD):** <each PRD [ASSUMPTION] that bears on structure> - _tier: uncertain_
- **Glossary terms used precisely:** <term - meaning>

<!-- ============================================================ STEP 2 -->
## 2. Core decisions

<!-- Category by category: data, auth/security, API/communication, frontend, infra.
     Use the decision block below. Write UNKNOWN where you don't know - do not
     invent. Curate EACH into the ledger as you go and fill the Ledger: line. -->

### D-1: <the decision, one line>
- **Choice:** <what was chosen - or `UNKNOWN` with the open question>
- **Tier:** uncertain | tentative | confirmed
- **Evidence:** <data points / spike / prior art - name them; a spike id if confirmed>
- **Affects:** <FRs / components, e.g. FR-3, billing component>
- **Alternatives considered:** <rejected option - why (one line each)>
- **Ledger:** led-NNNN

### D-2: <...>
- **Choice:**
- **Tier:**
- **Evidence:**
- **Affects:**
- **Alternatives considered:**
- **Ledger:** led-NNNN

<!-- To change D-1 later, DO NOT edit it. Append a new block, e.g. D-9, with:
     - **Supersedes:** D-1 - <why it changed (new evidence)>
     and supersede its ledger entry too. -->

<!-- ============================================================ STEP 3 -->
## 3. Constraints (enforced by the adversarial critic)

<!-- Rules that must hold across the whole build. These are what
     episteme:adversarial-critic rejects diffs against, so each must be a
     CHECKABLE rule, not a vibe. Curate each as a `constraint` ledger entry. -->

### C-1: <checkable rule, e.g. "all DB access goes through the repository layer">
- **Tier:** uncertain | tentative | confirmed
- **Evidence:** <preference -> assumed; a measured failure/spike -> verified, cite it>
- **Affects:** <which layers/modules>
- **Ledger:** led-NNNN

### C-2: <e.g. "the domain layer never imports from the web layer">
- **Tier:**
- **Evidence:**
- **Affects:**
- **Ledger:** led-NNNN

<!-- ============================================================ STEP 4 -->
## 4. Components & structure

<!-- Components and their boundaries; the interfaces each exposes; and the mapping
     of PRD FRs/epics to where they live. Tier each boundary. Interfaces named
     here become the surface episteme:writing-the-contract turns into oracles. -->

### Components

- **<component / module / service>** - responsibility: <one line>. _tier: <...>_
  - Interfaces: `<public function / endpoint / type / event signature>`
  - Boundary: <what it must NOT reach into>

### FR / epic -> location mapping

| PRD item | Lives in | Tier |
|---|---|---|
| FR-1 | `<path / module / service>` | <tier> |
| FR-2 | `<...>` | <tier> |

<!-- ============================================================ STEP 5 -->
## 5. Risks & open questions

<!-- Silence-over-speculation made into a deliverable. Every UNKNOWN from above,
     the spike that would resolve it (cheapest experiment that earns `confirmed`),
     and the risks of the bets you took. Each blocking open question is also an
     `assumption` ledger entry stating what evidence would resolve it. -->

### Open questions (UNKNOWNs to resolve)

- **OQ-1:** <the unknown> - resolving spike: <cheapest experiment>; blocks: <FR/story>; ledger: led-NNNN
- **OQ-2:** <...>

### Risks (of the bets taken)

- **R-1:** <risk of an `uncertain`/`tentative` decision> - mitigation / trigger to revisit: <...>

<!-- ============================================================ STEP 6 -->
<!-- COMPLETE: integrity pass (every decision has a tier + Ledger id; no section
     overwrote an earlier one; every UNKNOWN appears in §5; ledger-check printed OK),
     set stepsCompleted: [0,1,2,3,4,5,6] and status: complete, then hand off to
     episteme:sharding-into-stories. -->
