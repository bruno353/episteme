---
inventory: .episteme/behavior-inventory.md  # source artifact: capabilities, behaviors, quirks, coupling facts
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
status: draft                               # draft | adjudicated | superseded
---

<!--
  Episteme Parity Map (Migration track, phase M-B - spec). Authored by
  episteme:adjudicating-parity from .episteme/behavior-inventory.md + the ledger.
  Replaces the PRD for migrations. Hands off to episteme:deciding-architecture
  (brownfield) and then episteme:sharding-into-stories (slices -> stories).

  THE EPISTEMIC THROUGH-LINE (do not drop any of the three):
  1. PARITY IS THE NULL HYPOTHESIS. Every capability carries exactly ONE decision
     (retire | retain-on-legacy | migrate-as-is | migrate-and-fix | repurchase)
     with cited evidence. Nothing migrates because it exists.
  2. EVERY QUIRK IS ADJUDICATED preserve-or-fix BY A NAMED HUMAN (the agent
     proposes, a human decides, the log records who/when/why). Preserved quirks
     enter the slice's equivalence contract; fixed quirks become their own
     oracle-backed AC. Unadjudicated quirks block their capability's slice.
  3. AUTHORITY SURVIVES. A behavior still `assumed` in the inventory that a slice
     depends on gets a Capture-first: flag and a capture spike BEFORE that slice's
     contract - equivalence to a guess is not equivalence.

  Every decision/adjudication below is ALSO a ledger `decision` entry via
  episteme:curating-the-ledger (sole owner - never write ledger.jsonl yourself).
  Human adjudications cite "human decision - <who>, <date>, parity-map Q-N" as
  source. Lineage: adapts Patterns of Legacy Displacement (Fowler et al.) and the
  industry retire/retain/repurchase taxonomy - credited, not copied.
-->

# Parity Map: <legacy system / module> -> <target system>

## 0. Document Purpose

<!-- 1 paragraph: which legacy scope this adjudicates (e.g. "the VB6 invoicing
module moving to a NestJS service"), which behavior inventory and ledger entries
it builds on, and who consumes it downstream (architecture, story sharding, the
equivalence contracts). -->

## 1. Decision Summary

<!-- One row PER capability from the inventory - ids VERBATIM, none dropped, no
renumbering. This is the at-a-glance audit surface; §2 holds the detail. A
capability with no row, or a decision outside the five-word vocabulary, fails
the Iron Law. -->

| Cap | Capability | Decision | Slice | Quirks (status) | Ledger |
|-----|-----------|----------|-------|-----------------|--------|
| CAP-1 | <name> | retire | - | - (moot) | `led-NNNN` |
| CAP-2 | <name> | retain-on-legacy | - (behind seam) | - (moot) | `led-NNNN` |
| CAP-3 | <name> | migrate-as-is | S-1 | Q-2 preserved | `led-NNNN` |
| CAP-4 | <name> | migrate-and-fix | S-2 | Q-6 preserved, Q-7 fix | `led-NNNN` |
| CAP-5 | <name> | repurchase | S-3 (integration only) | - (moot) | `led-NNNN` |

## 2. Capability Decisions

<!-- One block per capability. The parity-challenge gate must have been run for
every migrate-* decision: who used it (evidence)? what breaks without it? does an
off-the-shelf product cover it? is retaining cheaper for now? Evidence refs cite
inventory ids (CAP-NN verbatim from the inventory; Q-NN verbatim from its Quirk
register) and ledger ids with their authority (verified/assumed). Rationale must
be auditable by a reviewer who was not in the room. -->

### CAP-1: <capability name>

- **Decision:** retire
- **Evidence:** <usage logs / call counts / owner confirmation, with ledger id +
  authority - e.g. "led-0012 (verified - zero invocations in 14 months of audit
  logs); owner sign-off: <role>, <date>">
- **Rationale:** <why it ends - what was checked for hidden consumers>

### CAP-2: <capability name>

- **Decision:** retain-on-legacy
- **Evidence:** <low value / low change-rate evidence>
- **Rationale:** <why it is not worth migrating in this program>
- **Reopen condition:** <the change that would put it back on the table - e.g.
  "legacy runtime EOL announced, or change requests exceed N/quarter"> (recorded
  in the ledger entry)

### CAP-4: <capability name>

- **Decision:** migrate-and-fix
- **Evidence:** <captured-corpus refs (CAP-NN capture, authority) + consumer evidence>
- **Rationale:** <why it survives the parity challenge AND which captured
  behavior is adjudicated a bug>
- **Quirks:**
  - **Q-6** <one-line captured behavior> -> **PRESERVE** - human decision:
    <name/role>, <date>. "<why downstream depends on it>". Ledger: `led-NNNN`.
  - **Q-7** <one-line captured behavior> -> **FIX** - human decision:
    <name/role>, <date>. New behavior (testable): <the intended outcome an
    oracle can decide>. Override: `par-NNNN` (§4). Ledger: `led-NNNN`.
- **Slice:** S-2

<!-- ...one block per capability... -->

## 3. Quirk Adjudication Log

<!-- One row PER quirk of every migrate-* capability (quirks of retired/retained
capabilities are moot - say so in §1). Quirk ids are Q-NN, verbatim from the
inventory's Quirk register. The agent PROPOSES with evidence both ways; a HUMAN
decides; the row records who/when/why. A `fix` decision mints an adjudicated
override in §4 (`par-NNNN`). A row with decision `open` blocks its capability's
slice contract (list it in §8). No agent-only adjudications. -->

| Quirk | Cap | Captured behavior (verbatim ref) | Agent proposal | Decision | Decided by | Date | Rationale | Ledger |
|-------|-----|----------------------------------|----------------|----------|------------|------|-----------|--------|
| Q-6 | CAP-4 | <CAP-4 capture: per-line tax rounding drifts up to $0.02/invoice> | preserve | **preserve** | <name/role> | <date> | <ERP reconciles against legacy totals> | `led-NNNN` |
| Q-7 | CAP-4 | <CAP-4 capture: negative quantities accepted, produce negative tax> | fix | **fix** | <name/role> | <date> | <no consumer depends on it; new behavior: reject with validation error - override `par-NNNN`> | `led-NNNN` |
| Q-9 | CAP-3 | <...> | preserve | **open** | - | - | <human unavailable - BLOCKS S-1 contract> | - |

## 4. Adjudicated Overrides (par-NNNN)

<!-- One row per fix-adjudicated quirk. These are the ONLY legitimate divergences
from the captured legacy outputs: verifying-equivalence resolves each corpus
entry's expected output adjudicated-override-first, legacy-capture otherwise. The
capture itself is never edited - the override sits beside it. Every `fix`
decision in §3 mints exactly one row here, with the new expected behavior stated
testably. -->

| Override | Q-NN it implements | Corpus scope (which entries/inputs) | Expected output in the NEW system (testable) | Decided by (human, date) | Ledger |
|----------|--------------------|--------------------------------------|----------------------------------------------|--------------------------|--------|
| par-0001 | Q-7 | <entries 0107, 0212 - negative-quantity orders> | <rejected with a validation error; no tax row written> | <name/role>, <date> | `led-NNNN` |

## 5. Slice Plan

<!-- Ordered VALUE-STREAM slices (end-to-end flows a user/downstream system cares
about), never technical layers. Each slice cuts over independently and is
independently reversible - a slice with no rollback story is a small big-bang.
Feasibility notes cite the inventory's coupling facts BY ID (shared DB tables,
COM/interop deps, cross-module globals, batch timing); these same facts feed the
policy's reachability audit downstream, so cite, do not summarize. -->

### S-1: <value-stream name, e.g. "quote-to-invoice">

- **Order:** 1 (no dependencies)
- **Capabilities:** CAP-3 (migrate-as-is); seam respects CAP-2 (retained on legacy)
- **Cutover:** <mechanism - routing rule / feature flag / dual-run with output
  comparison, and for whom>
- **Reversibility:** <how this slice rolls back if cutover fails - what is
  switched, what data is reconciled>
- **Feasibility notes (coupling facts):**
  - <CAP-NN / led-NNNN: e.g. "invoicing and inventory write the same STOCK table -
    this slice needs a sync strategy or CAP-7 moves in the same slice">
  - <...>
- **Capture-first:** <CAP-NN (assumed) - capture spike SP-1 precedes this slice>
  *(omit if none)*

### S-2: <value-stream name>

- **Order:** 2 (after S-1: <why>)
- **Capabilities:** CAP-4 (migrate-and-fix: Q-6 preserved, Q-7 fixed)
- **Cutover / Reversibility / Feasibility notes / Capture-first:** <...>

<!-- ...one block per slice, in cutover order... -->

## 6. Capture-First Index

<!-- Every behavior whose authority is still `assumed` AND that a slice depends
on. Each gets a capture spike: run the legacy against recorded inputs, capture
outputs, hand the finding to the curator to flip `assumed` -> `verified`. The
dependent slice's contract is NOT written until its corpus exists. -->

| Behavior | Authority | Blocks | Capture spike | Done when |
|----------|-----------|--------|---------------|-----------|
| CAP-NN <one-line> | assumed (<source: code reading / folklore>) | S-2 contract | SP-1: <record inputs X, capture outputs Y on legacy> | ledger entry flipped to `verified` with the corpus as oracle_ref |

## 7. Out of Scope

<!-- The value of this phase lives here. If this section is empty, parity won by
default and the map fails its job. -->

### 7.1 Retired (will not exist in the new system)
- CAP-1 <name> - evidence: <led-NNNN>; sign-off: <role>, <date>

### 7.2 Retained on legacy (not migrated in this program)
- CAP-2 <name> - reopen condition: <...> (`led-NNNN`)

### 7.3 Dropped scope / explicit non-goals
- <anything the migration deliberately does not attempt - new features, platform
  changes, performance work beyond equivalence - with a one-line reason>

## 8. Open Questions & Blockers

<!-- Numbered. Every `open` quirk appears here with the slice it blocks. Honest
unknowns -> future adjudication sessions or capture spikes, not silent gaps. -->

1. Q-9 is `open` (no adjudicator available) - BLOCKS the S-1 contract for CAP-3.
2. <unknown>

---

**Closure verdict:** `Adjudication: <N> capabilities, all decided; <M> quirks,
all adjudicated` - OR - list every capability without a decision and every quirk
without a named-human adjudication as a GAP (the map then FAILS the Iron Law and
must not hand off; `open` quirks are allowed only if §8 names them and their
blocked slices). Also confirm: every decision/adjudication has its ledger entry
(`ledger-check` clean), every `fix` quirk has its `par-NNNN` override in §4,
every slice has cutover + reversibility + cited coupling facts, and every
`assumed` dependency has a capture spike ordered before its slice.
