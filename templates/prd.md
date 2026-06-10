---
title: <Product / Feature name>      # working title - confirm
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
status: draft                         # draft | active | superseded
---

<!--
  Episteme PRD (Full track, phase 2 - spec). Authored by episteme:writing-a-prd
  from .episteme/brief.md. Hands off to episteme:deciding-architecture.

  THE EPISTEMIC THROUGH-LINE (do not drop any of the three):
  1. Every FR's "Consequences (testable)" must be phrased as OBSERVABLE outcomes,
     so episteme:writing-the-contract can lift each into an acceptance criterion
     PAIRED WITH A CHEAP ORACLE (test/type/lint/build/command/manual). You write
     the WHAT to observe, not the oracle itself.
  2. Every [ASSUMPTION: ...] tag below MUST also become an `assumption` entry in
     .episteme/ledger.jsonl via episteme:curating-the-ledger (authority: assumed).
     The tag is a pointer; the ledger is the durable home.
  3. State a requirement firmly ONLY if a `verified` ledger finding backs it (cite
     it). A bet is marked [ASSUMPTION] and recorded `assumed`. Never launder a bet
     into a fact.

  Shape adapted from BMAD's bmad-prd (credited, not copied). Delete sections that
  do not earn their place; add Adapt-In clusters the product calls for.
-->

# PRD: <Product / Feature name>

## 0. Document Purpose

<!-- 1 paragraph: who this PRD is for (PM, architecture/story owners downstream),
how it's structured (Glossary-anchored vocabulary, FRs nested under features with
testable consequences, assumptions tagged inline + indexed + mirrored to the
ledger). Name any prior inputs (brief, UX, prior ledger findings) and where they
live - this builds on them, it does not duplicate. -->

## 1. Vision

<!-- 2-3 paragraphs: what this is, what it does for the user, why it matters.
Compelling enough to stand alone. -->

## 2. Target User

### 2.1 Jobs To Be Done
<!-- Bulleted. The jobs the user hires this product to do - functional, emotional,
social, contextual. "This is for me as the builder" is valid for a hobby project. -->

- <JTBD>
- <JTBD>

### 2.2 Non-Users (v1) *(optional - add when the audience boundary is non-obvious)*
<!-- Who this is explicitly NOT for in v1. -->

### 2.3 Key User Journeys *(optional - add when flows are non-obvious)*
<!-- Named-persona narratives. Numbered UJ-1..UJ-N. FRs reference them inline
("Realizes UJ-3"). Each: persona+context, entry state, path (3-5 beats), climax
(value delivered + how they know), resolution; optional one edge case. -->

- **UJ-1. <one-line title - persona doing the thing>**
  - **Persona + context:** <one line, grounded enough to explain the why>
  - **Entry state:** <authenticated? which surface? coming from where?>
  - **Path:** <3-5 concrete beats>
  - **Climax:** <the moment value lands and how the user knows>
  - **Resolution:** <state they are left in; what's next>
  - **Edge case** *(optional):* <one real failure mode + what the user does next>

## 3. Glossary

<!-- Every domain noun the rest of the doc uses, defined ONCE. From here on these
terms are used VERBATIM in FRs, UJs and metrics. A synonym anywhere is a discipline
violation - it confuses the downstream contract and critic. If §4 introduces a new
noun, add it here in the same pass. -->

- **<Term>** - definition; relationships to other terms; cardinality where relevant.
- **<Term>** - ...

## 4. Features

<!-- One coherent feature per subsection: behavioral description first, FRs nested.
FRs numbered globally FR-1..FR-N so downstream artifacts have stable references.
Use Glossary terms verbatim. Reference UJs by id where the chain matters. -->

### 4.1 <Feature name>

**Description:** <behavioral narrative - how it works, who uses it, the experience,
edge cases. Realizes UJ-X. Use Glossary terms exactly. Embed inline
`[ASSUMPTION: ...]` where you inferred without confirmation.>

**Functional Requirements:**

#### FR-1: <short capability name>

<Actor> can <capability> <under conditions>. Realizes UJ-X.

**Consequences (testable):**
<!--
  Each line is an OBSERVABLE outcome a cheap oracle could decide (asserted value,
  detected state, arithmetic/structural invariant, status code, required/forbidden
  pattern). NOT a feeling ("feels fast"), NOT an implementation step ("uses Redis").
  Genuinely subjective? Phrase it as what a reviewer inspects -> becomes a
  `manual:` oracle downstream. Gate every line: "what would someone run/observe to
  decide this true/false, and is that cheap?"
-->
- <observable outcome 1>
- <observable outcome 2>

**Out of Scope:** *(optional - what this FR explicitly does NOT cover; bounds the critic)*
- <bound>

#### FR-2: <short capability name>

<...>

**Feature-specific NFRs:** *(optional - only if any apply uniquely to this feature)*
- <performance / security / accessibility constraint specific to this feature>

**Notes:** *(optional - open questions specific to this feature, `[NOTE FOR PM]` callouts)*

### 4.2 <Feature name>

<...>

## 5. Non-Goals (Explicit)

<!-- Bulleted. What this product is NOT and will NOT do in v1. Does outsized work
downstream - prevents "let me also add this nearby thing" at every level. Broader
than per-FR Out of Scope: the "we are not building X / not becoming Y" statements. -->

- <non-goal>
- <non-goal>

## 6. MVP Scope

### 6.1 In Scope
<!-- Bulleted, crisp. -->

### 6.2 Out of Scope for MVP
<!-- Bulleted, each with a one-line reason where it matters. Mark v2/v3 deferrals
explicitly. `[NOTE FOR PM]` where a deferred item is load-bearing. -->

## 7. Success Metrics

<!-- Each SM cross-references the FR(s) it validates. Counter-metrics counterbalance
specific primary/secondary metrics - they stop the architect/dev optimizing the
wrong thing. Length scales with stakes: a hobby utility may need one sentence; a
launch needs targets + measurement method. -->

**Primary**
- **SM-1:** <metric> - definition, target. Validates FR-X, FR-Y.

**Secondary**
- **SM-2:** <metric> - definition, target. Validates FR-Z.

**Counter-metrics (do not optimize)**
- **SM-C1:** <metric> - why this must NOT be optimized. Counterbalances SM-1.

## 8. Open Questions

<!-- Numbered. Honest unknowns -> future tickets / follow-up research, not silent
gaps. An Open Question that is also a working bet should appear in §9 too. -->

1. <unknown>
2. <unknown>

## 9. Assumptions Index

<!--
  EVERY [ASSUMPTION] from the document, surfaced for explicit confirmation - AND
  each one mirrored to a ledger `assumption` entry. Do NOT write ledger.jsonl
  yourself; hand these to episteme:curating-the-ledger (sole owner), which runs
  ledger-check. Suggested entry per row:
    {type: assumption, authority: assumed, source: "prd.md §4.x FR-n",
     statement: "<the assumption>", feature: "<contract slug if known>"}
  When a spike/stakeholder/test later confirms one, the curator supersedes it with
  a `verified` entry - that flip is why the ledger, not this index, is the truth.
-->

| # | Assumption (from §) | Statement | Ledger entry | Status |
|---|---|---|---|---|
| A-1 | §4.1 FR-1 | <the inferred bet, one sentence> | `led-NNNN` (assumed) | curated / pending |
| A-2 | §4.2 FR-3 | <...> | `led-NNNN` (assumed) | curated / pending |

<!--
  ====================================================================
  ADAPT-IN MENU - add only the clusters the product calls for.
  (Adapted from BMAD's bmad-prd adapt-in menu.)
  --------------------------------------------------------------------
  Cross-cutting:   Cross-Cutting NFRs | Constraints & Guardrails (safety/
                   privacy/cost) | Why Now
  Consumer:        Aesthetic & Tone | Information Architecture | Monetization |
                   Platform (web/mobile/PWA/native; v1 vs v2)
  Enterprise:      Stakeholders & Approvals | Risk & Mitigations | ROI / Business
                   Case | Operational Requirements (SLA/RTO/RPO) | Integration &
                   Dependencies | Rollout & Change Mgmt | Data Governance |
                   Audit Trail / Decision Provenance
  Regulated:       Compliance & Regulatory (HIPAA/PCI/GDPR/SOC2/WCAG/...)
  Developer prod:  API Contracts / Public Surface | Versioning & Deprecation |
                   Performance Budgets | Language/Runtime Targets & Deps
  Embedded/HW:     Hardware Constraints | Deployment & Update Mechanism |
                   Environmental & Reliability Requirements
  --------------------------------------------------------------------
  Whatever you add, keep the through-line: any NFR/constraint with a testable
  bound gets phrased as an observable outcome (it becomes an AC downstream); any
  it-rests-on-X bet gets an [ASSUMPTION] tag + a ledger entry.
  ====================================================================
-->
