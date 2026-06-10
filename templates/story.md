---
id: story-<NN>                          # e.g. story-12; unique within the project
epic: <epic-id>                         # the epic in .episteme/epics.md this story belongs to
title: <short story title>
status: draft                           # draft | ready-for-dev | contracted | in-progress | done
realizes_frs: []                        # e.g. [FR-3, FR-7]; the PRD functional requirements this story delivers
contract: null                          # set to contract-<slug> once writing-the-contract has run; null until then
---

<!--
  A self-contained, ready-for-dev story. Authored by episteme:writing-a-story from ONE
  story in .episteme/epics.md. Lineage: BMAD bmad-create-story (As-a/I-want/so-that,
  Given/When/Then ACs, Tasks linked to AC#, Dev Notes, References, Dev Agent Record),
  adapted: ACs are phrased to become ORACLE-BACKED contract criteria, and the story
  carries an explicit Known facts vs Open assumptions split from the ledger.
  This story HANDS OFF its Acceptance Criteria to episteme:writing-the-contract,
  which pairs each AC with a cheap oracle authored blind to the implementation.
-->

# Story <NN>: <title>

## Story

As a <role>,
I want <action>,
so that <benefit>.

## Acceptance Criteria

<!--
  ONE observable behavior per AC (if it says "and", split it). Phrase each so it can
  become an oracle-backed contract criterion: a concrete, decidable outcome a cheap
  gate (test/type/lint/build/command) could check. NO "should work" / "be robust".
  Map each AC to the FR(s) it realizes. Do NOT write oracles here - that is
  writing-the-contract's job (authored blind). Given/When/Then is the preferred shape.
-->

- AC-1 (realizes: FR-<n>): Given <precondition>, when <action>, then <observable, decidable outcome>.
- AC-2 (realizes: FR-<n>): Given <precondition>, when <action>, then <observable, decidable outcome>.
- AC-3 (realizes: FR-<n>, error case): Given <bad input/state>, when <action>, then <specific failure: status code / error type / message>.

## Tasks / Subtasks

<!-- Each task names the AC(s) it advances. These are work hints for the implementer; the loop still does one change at a time and lets the oracle decide. -->

- [ ] Task 1 (AC: #) - <what to do>
  - [ ] Subtask 1.1 - <step>
- [ ] Task 2 (AC: #) - <what to do>

## Dev Notes

<!--
  The minimum context to implement WITHOUT re-reading the whole architecture.
  Pull from .episteme/architecture.md and the codebase. Cite every technical claim
  in References. Do not invent paths - if you have not confirmed a path exists,
  it goes under Open assumptions below, not stated here as fact.
-->

- Relevant architecture decisions and constraints (from architecture.md), with their authority.
- Source files / modules to touch (confirmed to exist), with path.
- Interfaces this story must expose or consume (names; the contract will pin them down).
- Testing approach the codebase already uses (runner, fixture conventions) - so the contract's oracles are runnable.

### Known facts vs Open assumptions

<!--
  THE EPISTEMIC SPINE OF THE STORY. Split what this story depends on by ledger authority.
  - Known facts = `verified` ledger entries (oracle/observation backs them). Cite led-id + source.
  - Open assumptions = `assumed` ledger entries OR things not yet in the ledger that this story
    needs to be true. Each must name what would VERIFY it (a discriminator). These are what the
    policy must probe before it can go `ready`, and what the contract's oracles will pin down.
  Never list an assumption under Known facts. If unsure, it is an assumption.
-->

**Known facts (verified - this story relies on them):**
- [led-<id>] <fact> - source: <where>, oracle_ref: <command/test>

**Open assumptions (assumed / not yet verified - this story depends on them):**
- [led-<id> | NEW] <assumption> - to verify: <the cheap discriminator: a test, grep, probe>

### Project Structure Notes

<!-- Alignment with the architecture's structure (paths, modules, naming). Note any detected conflict or variance with rationale. -->

- <alignment / conflict / variance + rationale>

## References

<!-- Cite EVERY technical detail in Dev Notes with a source path and section. -->

- [Source: .episteme/epics.md#<epic-id>] - the epic this story was sharded from
- [Source: .episteme/prd.md#FR-<n>] - the functional requirement(s) realized
- [Source: .episteme/architecture.md#<section>] - architecture decision relied on
- [Source: <codebase/path#symbol>] - source file/symbol confirmed to touch

## Handoff

This story is ready when every AC is an observable behavior mapped to its FR, Dev Notes
cite their sources, and the Known facts vs Open assumptions split is honest.

**Next:** hand the Acceptance Criteria to `episteme:writing-the-contract`, which pairs
each AC with a cheap oracle authored blind to the implementation and writes
`.episteme/contract.md`. From there the loop runs: synthesizing-the-policy ->
implementing-a-story <-> verifying-against-contract -> adversarial-critic ->
curating-the-ledger.

## Dev Agent Record

<!-- Filled by the implementer/loop during development. Empty at authoring time. -->

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
