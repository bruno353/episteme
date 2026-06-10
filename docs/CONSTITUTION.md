# Episteme - Constitution (v0.2)

> **Episteme** - the framework (the all-in-one: skills, tools, and a spec-driven
> dev method). **Metis** (**M**ulti-agent **E**pistemic **T**yped-ledger
> **I**nvestigation **S**ynthesis) - the name of the epistemic flow/architecture
> inside it (hypotheses, falsification, curated memory, factual verdicts), distilled
> from our ARC-AGI-3 agent work. In Greek thought, *episteme* is justified knowledge;
> *Metis* is practical wisdom/cunning - the knowledge and the craft of applying
> it. Metis is the engine; Episteme is the framework it powers.

## One-line positioning

**The epistemic control layer for agentic software development.** Episteme takes
the full spec-driven lifecycle that BMAD pioneered and the execution discipline
that Superpowers refined, and threads through both an epistemic control loop - **Metis** - so
that "done" is *proven against a contract* instead of *declared by the agent*.

## The problem (what BMAD, Superpowers and SDD leave on the table)

These are excellent tools. Episteme does not compete with their *workflow*; it
adds the *control* layer they only gesture at.

| | BMAD | Superpowers |
|---|---|---|
| Organizing unit | Roles (PM, architect, dev, QA) | Competencies (skills) |
| Planning | Heavy: PRD + architecture -> sharded stories (YAML) | Light: brainstorm -> 2-5 min task plan |
| Execution | Sequential, file-based handoffs | TDD iron law, fresh subagent per task, worktrees |
| Strong at | Greenfield, formal traceability, self-contained stories | Execution discipline, context hygiene, self-evolving |
| Epistemic gestures | `[ASSUMPTION]` tags, adversarial-review skills, decision-log | `verification-before-completion` (evidence before claims) |
| What's missing | The gestures are bolt-on skills, not a woven spine | No durable memory; verdicts are binary pass/fail |

**The four gaps both leave open (the pillars Metis fills):**

1. **The contract is not the enforced source of truth.** BMAD even calls its spec a
   "Canonical contract" with testable success - so a contract *existing* is not the
   gap. The gap is that nobody *adversarially verifies the diff against it* by
   default, and nobody runs the "two agents that don't see each other" pattern: the
   oracle/test author writes tests from the contract *blind to the implementation*,
   and a *separate* post-diff critic audits compliance.
2. **No curated memory.** BMAD's `.decision-log.md` is a flat audit trail;
   Superpowers' fresh-subagent approach throws context away. Neither has a typed
   ledger with source, freshness and authority that survives handoffs.
3. **No mandatory fact/hypothesis separation.** BMAD's `[ASSUMPTION]` tags are
   optional; neither forces "I verified this" vs "I assume this." Hypotheses
   silently become facts.
4. **No explicit oracle doctrine.** Neither states when to trust a cheap
   deterministic gate (tests/types/lint/CI) versus LLM judgment.

## Metis - the epistemic loop

Metis is the control architecture distilled from `world_model_agent_v2` (our
ARC-AGI-3 research agent; that codebase is private, but the architecture is fully
described here and in docs/METIS.md). It is a
set of **voices** (each a typed role with its own cadence) writing to and reading
from a **curated ledger**, where the harness never judges progress - the voices
do - and every claim is separated into fact, hypothesis, or uncertainty.

The wmv2 voices map cleanly onto software-dev roles:

| wmv2 voice | Episteme role | What it does |
|---|---|---|
| Investigator | Fact-gatherer | reads ground truth via cheap oracles (tests/types/lint/grep) |
| Tactical | Implementer | predict -> act -> observe, one change at a time (TDD) |
| Verifier | Oracle verdict | did the change do what was predicted? factual, not "is it good" |
| Critic | Adversarial reviewer | checks work against the CONTRACT, reading the contract not the code |
| Curator | Ledger keeper | consolidates durable decisions/constraints with authority + freshness |
| Theorist | Architecture model | slowly-evolving codebase/domain structure; confidence tiers; silence over speculation |
| Operational Policy | Gated planner | synthesizes a candidate plan from known facts, but refuses `ready` unless every step rests on evidence; audits reachability; reconciles against the prior plan; advisory, never commanded |

**The loop, per story:** gather facts -> separate fact/hypothesis -> write or
confirm the contract -> synthesize a gated policy (readiness + reachability +
retrospective + discriminators) -> implement (predict + act + observe) -> verdict
(cheap oracle) -> adversarial critic vs the contract -> curate the ledger.

## The four pillars (what Metis enforces)

1. **Contract-as-truth.** Every story carries a machine-checkable contract:
   acceptance criteria as invariants, interfaces, error taxonomy. The contract,
   not the agent's word, defines "done." Implementer and verifier both read it.
2. **Curated ledger (memory as a system).** A typed ledger holds named entries -
   decisions, constraints, expensive findings - each tagged with source,
   freshness and authority. It persists across handoffs. For management, it is
   also a free audit trail.
3. **Adversarial verification with epistemic separation.** The verifier reads the
   contract, never the implementer's reasoning. Output separates `visible_facts`
   from `hypotheses`, lists evidence for and against, and names the next
   falsifiable test. Uncertainty is preserved, never laundered into a fact.
4. **Right-oracle doctrine.** Prefer the cheapest reliable oracle. In code that
   means deterministic gates - tests, types, lint, CI - are the trust spine; LLM
   judgment is reserved for where no cheap oracle exists (design, ambiguity).

> **Honest note (this is a feature, not a bug):** Pillar 4 *inverts* a doctrine
> we learned in a domain with no ground truth (ARC-AGI-3), where deterministic
> guards were fragile proxies and judgment had to go to the LLM. Software has
> cheap oracles that domain lacked. Knowing which learnings transfer and which
> invert is the point - and saying so openly is a credibility asset.

## Lineage (credited, not hidden)

Episteme stands on the shoulders of, and interoperates with:

- **BMAD** (MIT) - the full SDD lifecycle and the PRD/architecture/story scaffolding we adopt.
- **Superpowers** (MIT) - the skills-as-files model and execution discipline.
- **Pi** (MIT) - provides a typed NDJSON session ledger (a `SessionEntry` tree + compaction). Pi does NOT have source/authority/freshness; our phase-2 extension adds that epistemic layer on top of Pi's `SessionManager`. Validates Pillar 2 and is the phase-2 target.
- **Open standards** - SKILL.md / AGENTS.md so Episteme runs inside any harness.

Episteme is an original layer, not a fork. We reuse patterns and credit them; the
contribution that is ours is **the epistemic loop** (internally, *Metis*) - binding
contract + typed ledger + gated policy + factual verifier + adversarial critic
into one *mandatory* flow that none of BMAD/Superpowers/Pi enforces by default.

## What v1 is (locked decisions)

- **Surface:** portable skills first (SKILL.md, runs in Claude Code / Superpowers
  today). The deeper Pi extension (TypeScript over the typed ledger) is phase 2.
- **SDD scope:** the full pipeline - brief -> PRD -> architecture -> sharded
  stories - BMAD-level completeness, every artifact instrumented by the loop. A
  lighter "Quick" track (intent -> contract -> implement -> verify) for small apps.
- **Driver:** OSS credibility AND real usability by small internal teams building mini-apps.

## Why this helps small internal teams build mini-apps

| Real failure | Pillar that fixes it |
|---|---|
| "The agent said it's done, but it isn't" -> trust erodes | Contract-as-truth + critic verifies against the contract, not self-report |
| Agent drifts from the ask / invents scope | Contract + critic catch the drift |
| Agent forgets decisions made earlier in a long task | Curated ledger persists decisions with source + freshness |
| Each dev's agent does it differently | Team standards become versioned skills, not a wiki nobody reads |
| Management has no trail of what/why was decided | The ledger *is* the audit trail |

The strongest trust unlock for non-technical users is Pillar 3: the agent shows
"this I verified / this I assume," so even a non-programmer can see what is solid.

## Non-goals (honesty keeps us credible)

- Not a new harness. Episteme rides inside Claude Code / Codex / Pi.
- Not a BMAD/Superpowers replacement. It is the control layer they lack; it can run alongside them.
- Not heavy epistemic machinery everywhere. Where a cheap oracle exists, we use it (Pillar 4).

## Roadmap

- **Phase 1 (v1):** portable skills - the full SDD pipeline + Metis. Reference clones of BMAD/Superpowers/Pi in `reference/` (read-only, gitignored).
- **Phase 2:** Pi extension/package implementing the typed ledger and critic as real TypeScript over Pi's `AgenticodingState`.
