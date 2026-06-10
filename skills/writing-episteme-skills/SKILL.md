---
name: writing-episteme-skills
description: Use when creating or editing an Episteme skill (a new voice, a lifecycle phase, or a tool wrapper) - so it matches the house format and plugs into the .episteme/ artifacts and the four pillars correctly.
---

# Writing Episteme skills

How to author a skill that fits Episteme. This is about authoring quality and
structural fit, not about evaluating prompts - the gate for a new skill is that it is
well-formed, connects to the artifacts correctly, and passes `plugin-check`.

## The Iron Law

```
A NEW SKILL IS NOT DONE UNTIL:
  1. tools/plugin-check.py passes (frontmatter valid, name == folder), and
  2. it reads/writes the canonical .episteme/ artifacts (never invents a new home), and
  3. it respects the four pillars (below) - it does not let a hypothesis become a fact.
```

## SKILL.md format (match the house style)

Study any existing Episteme skill (the format follows the Superpowers SKILL.md
conventions - Iron Laws, trigger descriptions, rationalization tables).

- **Frontmatter**: `name` (== the folder, kebab-case) + `description`. The
  description is a **trigger** ("Use when ...") - the situation that should make the
  agent reach for the skill - NOT a summary of what the skill does. (A summary makes
  the agent follow the description instead of reading the body.)
- **Body**: progressive disclosure. Lead with the core principle. Use an **Iron Law**
  + a **rationalization table** ("Excuse | Reality") only where the skill must hold a
  line under pressure. Give concrete numbered steps and good/bad (✅/❌) examples.
- English. Single hyphens, never em-dashes. Invoked as `episteme:<name>`.

## Episteme-specific requirements

1. **Connect to the artifacts.** Name exactly which `.episteme/` files you read and
   write (see `develop`'s canonical layout). Do not invent a new artifact path.
2. **Respect ledger ownership.** Only `curating-the-ledger` writes
   `.episteme/ledger.jsonl`. Other skills read it; if your skill produces a durable
   fact/decision, hand it to the curator, do not write the ledger yourself.
3. **Honour the four pillars** (see docs/CONSTITUTION.md):
   contract-as-truth, curated ledger (authority: `verified` vs `assumed`),
   adversarial verification, right-oracle. A skill that lets an `assumed` thing read
   as `verified` is wrong.
4. **Place it.** A loop *voice* gets wired into `develop`'s loop + listed in
   `using-episteme`. A standalone helper just needs to be invocable. A *tool* (a
   deterministic validator) goes in `tools/` mirroring `ledger-check.py`, with a
   schema in `schemas/` if it validates a shape.

## Steps

```
1. Decide the kind: voice (in the loop), lifecycle phase, standalone helper, or tool.
2. Pick the name = folder name: gerund for voices/lifecycle skills (the orchestrator
   `develop`, the bootstrap `using-episteme` and role-named voices like
   `adversarial-critic` are the exceptions). Confirm it does not collide.
3. Write SKILL.md: trigger description + the body (principle, steps, examples).
4. Wire it: if a voice, add it to develop's loop + using-episteme; if a tool, add the
   validator + schema and reference it from the relevant skill.
5. Run tools/plugin-check.py - it must pass (frontmatter, name==folder, hook intact).
6. Sanity-check the trigger: read the description as the agent would and confirm it
   fires in the intended situation and stays quiet otherwise.
```

## Red flags - STOP

- A `description` that summarizes the workflow instead of naming the trigger.
- A skill that writes `.episteme/ledger.jsonl` directly (only the curator may).
- Inventing a new artifact path instead of using the canonical `.episteme/` layout.
- Claiming the skill is done without a green `plugin-check`.

## What this skill deliberately does NOT do

It does not replay or "eval" prompts against fixtures. Skill quality here is judged by
format fit, artifact wiring, pillar compliance, and the deterministic `plugin-check` -
not by an evaluation harness over the skill's own text.
