---
name: using-episteme
description: Read at session start. Explains that you have Episteme - the epistemic control layer - and when to reach for the loop vs an individual voice.
---

# You have Episteme

Episteme is an epistemic control layer for coding. Its one rule:

> **"Done" is proven against a contract by a cheap oracle and an independent
> critic - never declared by the implementer.**

## When to use it

- **Building a feature or bugfix of any real substance** -> invoke `develop`
  (the orchestrator). It picks a track: **Quick** (a mini-app / single feature) goes
  straight to the loop (contract -> policy -> implement <-> verify -> critic ->
  curate); **Full** (greenfield / large) runs the lifecycle first (brief -> PRD ->
  architecture -> stories) then the loop per story. Artifacts live in `.episteme/`.
- **The Full-track lifecycle skills** (driven by `develop`, also invocable alone):
  `writing-a-brief`, `writing-a-prd`, `deciding-architecture`,
  `sharding-into-stories`, `writing-a-story`.
- **You need just one step** -> invoke that voice directly:
  - `writing-the-contract` - turn a vague ask into a verifiable contract (each
    acceptance criterion paired with a cheap oracle, authored before the code).
  - `synthesizing-the-policy` - decide the next move only when the evidence
    supports it (gated readiness, reachability, retrospective).
  - `implementing-a-story` - one change at a time, predict then verify.
  - `verifying-against-contract` - run the oracle; emit a factual verdict.
  - `adversarial-critic` - audit a diff against the contract (not the reasoning).
  - `curating-the-ledger` - record a decision/finding to durable memory.

If a task is trivial (a typo, a one-line obvious fix), you don't need the loop.
For anything where "did this actually work?" matters, you do.

## The four pillars (why it works)

1. **Contract-as-truth** - the contract, not your word, defines done.
2. **Curated ledger** - typed memory in `.episteme/ledger.jsonl` with source +
   authority (`verified` vs `assumed`); a hypothesis never silently becomes a fact.
3. **Adversarial verification** - the critic reads the contract, not your code.
4. **Right oracle** - lean on cheap deterministic gates (tests/types/lint/build);
   reserve judgment for where no cheap oracle exists.

Don't announce all of this to the user - just follow it. When you invoke a skill,
say which one and why in one line.
