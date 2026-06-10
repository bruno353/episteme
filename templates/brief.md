---
id: brief-<project-or-feature-slug>     # e.g. brief-invoice-importer
status: draft                            # draft | active | superseded
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
ledger_seeded: false                     # flip to true only after ledger-check ran clean
---

<!--
  The brief turns a raw idea into a shared, honest picture of WHAT and WHY -
  never HOW. Adapt this structure to the product: drop sections that do not
  earn their place, add ones it needs. But the two epistemic sections -
  "Known facts" and "Assumptions (unverified)" - are MANDATORY and must never
  collapse into each other. That fact/hypothesis split is what makes this an
  Episteme brief, not a generic one.

  As you fill this in, SEED THE LEDGER (episteme:curating-the-ledger):
    - a "Known facts" item you actually observed  -> finding / verified  (with oracle_ref: the grep/file/command)
    - an "Assumptions" item (a product bet, a guess) -> assumption / assumed
    - a hard "Constraint"                            -> constraint (verified if observed, else assumed)
  Each brief item below should cite its ledger id, e.g. (led-0003), so the
  brief and the ledger never drift apart.

  See episteme:writing-a-brief. Hands off to episteme:writing-a-prd.
  Lineage: structure adapted from BMAD's product-brief; the epistemic spine is ours.
-->

# Brief: <project / feature name>

One or two sentences: what this is and the force behind building it now. WHAT, not HOW.

## Problem

What pain exists, who feels it, how they cope today, the cost of the status quo.
Be specific - real scenario, real frustration, real consequence. No invented urgency.

## Target users + jobs-to-be-done

Who this serves and the job they are hiring it to do. For each user type:

- **<user type>** - when <situation>, they want to <motivation>, so they can <outcome>.

Keep it vivid but brief. Mark unverified user claims as assumptions below, not facts.

## Goals

What success looks like, ideally measurable. What must be true for this to be worth building.

- <goal - observable / measurable where possible>

## Non-goals (explicit)

What this deliberately does NOT do, for this version. Load-bearing: downstream
(the PRD, the contract's "Out of scope") inherits these to bound scope drift.

- <thing it is explicitly out of scope to do>

## Constraints

Hard limits the solution must respect: tech stack, deadline, budget, platform,
data, regulatory, an existing system it must fit. Each one becomes a `constraint`
ledger entry.

- <constraint> (led-XXXX)

## Known facts (verified)

What is actually TRUE about the codebase / domain / current state, each backed by a
real observation - a file you read, a grep you ran, a command output, a doc you saw.
Every item here MUST cite its source and is seeded as a `finding` / `verified`
ledger entry with an `oracle_ref`. If you cannot name how you know it, it is NOT a
fact - move it to Assumptions.

- <observed fact> - source: `<grep/file/command>` (led-XXXX)

## Assumptions (unverified)

Product bets, guesses, and beliefs not yet backed by an oracle - the things a later
phase must validate. These are seeded as `assumption` / `assumed` ledger entries.
Keeping them here, separate from facts, is the point: a hypothesis must never be
read later as a settled fact.

- <assumption / bet> - why we believe it; what would confirm/kill it (led-XXXX)

## Open questions

What is still unknown and who/what could answer it. Feeds the PRD and the first
fact-gathering pass of the loop.

- <open question>
