# Episteme - Scaffold Design (historical record, pre-v0.1)

This is the preserved design document written BEFORE the v0.1 build. It synthesizes
the deep read of BMAD, Superpowers and Pi (study clones, not shipped) and the
decisions the build started from. **The shipped structure diverged in places**
(the real `skills/` tree is flat, some proposed skills were folded or dropped, and
more tools/templates shipped than listed here) - see the README for what exists
today. Kept as the design rationale and decision log.

---

## 1. What we borrow (from the reference analysis)

### From BMAD - the SDD spine
- 4-phase lifecycle: **analysis -> planning -> solutioning -> implementation**.
- Artifact templates: PRD (FRs with "Consequences (testable)", Glossary, `[ASSUMPTION]` index, counter-metrics), Architecture (append-only, step-driven), Story (As a/I want/so that, Given/When/Then ACs, Tasks linked to AC#, Dev Notes, References, Dev Agent Record), Epics (FR inventory -> Epic -> Stories).
- **Note (corrected):** BMAD's `bmad-spec` already calls the spec a *"Canonical contract"* with testable capability success (`reference/bmad-method/src/core-skills/bmad-spec/assets/spec-template.md:7`). So "a contract exists" is NOT our novelty.
- `.decision-log.md` audit trail; 3-level config merge (`customize.toml`); doc sharding; expansion packs; web-bundles; **Quick Dev** express path.

### From Superpowers - the discipline mechanics
- **SKILL.md format**: frontmatter `name` + `description`-as-trigger; progressive disclosure.
- **Iron Law** style + **rationalization tables**; **verification-before-completion** (evidence before claims) = embryo of our verdict pillar.
- **subagent-driven-development** (implementer + spec-reviewer + code-quality-reviewer, fresh context); session-start hook; multi-tool packaging; **writing-skills** meta-skill with pressure-testing.

### From Pi - the typed-ledger primitive
- Typed **NDJSON** session ledger: `SessionEntry` union, `id`/`parentId` **tree** (not linear), `CompactionEntry` (`firstKeptEntryId`), `CustomEntry` for extension state (`packages/coding-agent/src/core/session-manager.ts:32-149`). MIT.
- Lazy skills (one-line stub in prompt, full body on demand). Extensions in TypeScript via hooks + `registerCommand`/`registerTool`.
- **Pi does NOT have source/authority/freshness/supersedes** - that is exactly what our layer adds (in entry `details` + a `SessionManager` subclass in phase 2).

### The gap all three leave (the real differentiator)
None of them makes the epistemic discipline a **mandatory woven loop**. BMAD has a
canonical contract + adversarial-review *skills you may invoke*; Superpowers has
evidence-before-claims; Pi has a typed ledger primitive. Episteme's contribution is
not any single one of these - it is binding them into one enforced loop:

**contract + typed ledger (authority/freshness) + gated policy readiness + factual
verifier + adversarial critic** - every step, every story, by default.

---

## 2. The epistemic loop (internally: "Metis") - wmv2 voices -> SDD roles

| wmv2 voice | Episteme role | What it does |
|---|---|---|
| Investigator | Fact-gatherer (folded) | reads ground truth via cheap oracles (tests/types/lint/grep) |
| Tactical | Implementer | predict -> act -> observe, one change at a time (TDD) |
| Verifier | Oracle verdict | did the change do what was predicted? factual, not "is it good" |
| Critic | Adversarial reviewer (post-diff) | audits the diff against the CONTRACT for compliance/drift/architecture |
| Curator | Ledger keeper | consolidates durable decisions/constraints with authority + freshness |
| Theorist | Architecture model (folded) | slowly-evolving structure; confidence tiers; silence over speculation |
| Operational Policy | Gated planner | candidate plan from known facts; refuses `ready` w/o evidence; reachability audit; retrospective |

**Two agents that don't see each other (corrected):** the separation is between the
**oracle/test author** (writes the failing test from the contract, *blind to the
implementation*, at contract time) and the **implementer**. The **critic** is a
*separate, post-diff* reviewer for contract-compliance, drift and architecture - not
the same thing as the blind test author.

**Loop per story:** gather facts -> separate fact/hypothesis -> write/confirm contract
(+ author its oracles, blind) -> synthesize gated policy (`not_ready`/`probe_more`/
`policy_candidate`/`ready` + reachability + retrospective + discriminators) ->
implement (predict+act+observe) -> verdict (run the cheap oracle) -> adversarial
critic vs contract -> curate ledger.

---

## 3. Proposed directory structure (v1)

```
episteme/
├── README.md                       # positioning: Episteme (framework) + the epistemic loop
├── docs/
│   ├── CONSTITUTION.md             # the thesis (done)
│   ├── SCAFFOLD_PROPOSAL.md        # this file
│   └── METIS.md                    # the loop spec, voice-by-voice (done; internal name)
├── schemas/
│   ├── ledger.schema.json          # JSON Schema - single source of truth for the ledger
│   ├── contract.schema.md          # the contract.md structure
│   ├── policy.schema.json          # the PolicyReport
│   └── verdict.schema.json         # the Verdict
├── tools/
│   └── ledger-check.py             # Python validator: ledger.jsonl against ledger.schema.json
├── .claude-plugin/{plugin.json, marketplace.json}
├── hooks/session-start             # bootstrap: inject using-episteme
├── skills/
│   ├── using-episteme/             # bootstrap skill (read at session-start)
│   │   # --- SDD lifecycle (from BMAD, instrumented by the loop) ---
│   ├── 1-discovery/{writing-a-brief, researching}/
│   ├── 2-spec/
│   │   ├── writing-a-prd/          # PRD w/ testable FRs + mandatory facts/assumptions split
│   │   └── writing-the-contract/   # contract.md per feature + authors its oracles (blind to impl)
│   ├── 3-architecture/deciding-architecture/   # append-only, confidence-tiered (theorist, folded)
│   ├── 4-stories/{sharding-into-stories, writing-a-story}/   # story REFERENCES contract.md
│   ├── 5-implementation/{implementing-a-story, verifying-against-contract}/
│   │   # --- epistemic core (cross-cutting) ---
│   ├── curating-the-ledger/        # owns ledger.jsonl; authority+freshness; runs ledger-check
│   ├── separating-fact-from-hypothesis/
│   ├── synthesizing-the-policy/    # gated plan: readiness + reachability + retrospective + discriminators
│   ├── falsification-driven-testing/
│   ├── adversarial-critic/         # post-diff: contract compliance / drift / architecture
│       # --- meta ---
│   └── writing-episteme-skills/    # how to author skills (pressure-tested)
├── templates/{prd.md, contract.md, story.md, policy.json, verdict.json, critic-report.md}
└── prompts/{implementer, oracle-author, verifier, critic, curator}.md   # the epistemic voices
```

---

## 4. Two tracks (the "heaviness" decision)

- **Full track** (greenfield, serious features): all phases, full PRD/architecture/stories.
- **Quick track** (mini-apps, internal tools): no heavy PRD/architecture, but a
  **mandatory minimal spine** of five artifacts produced every run:
  `contract.md` (+ oracles) -> `ledger.jsonl` -> `policy.json` -> `verdict.json` ->
  `critic-report.md`. This spine is what we build and prove on a real mini-app FIRST,
  before expanding to the full SDD pipeline.

---

## 5. Decisions (locked)

1. **Loop form**: hybrid - an orchestrator skill (`episteme:develop`) sequences the voices, AND each voice is a standalone skill invocable on its own.
2. **Ledger**: typed JSONL with `ledger.schema.json` (JSON Schema) as the single source of truth, validated by a small Python `tools/ledger-check.py` (the first "tool" in skills+tools+spec). The SAME schema file feeds the phase-2 Pi (TS) extension, so only the validator runtime is Python, not the schema. v1 is no longer zero-dependency (needs Python + `jsonschema`) - accepted for robustness.
3. **Contract**: a separate `contract.md` per feature, referenced by stories. Each acceptance criterion is paired with its cheap oracle (test/type/lint/command); those oracles are authored blind to the implementation. The critic checks story-vs-contract drift; the curator versions the contract in the ledger.
4. **Voice roster**: 5 explicit skills - implementer, verifier, critic, curator, policy-synthesis. Theorist folds into the architecture skill; investigator folds into the fact-gathering step.
5. **Naming**: gerund, no prefix; all skills in the `episteme` namespace (`episteme:<skill>`). Public docs say "epistemic loop"; "Metis" is internal shorthand only.
6. **Start point**: build the Quick track minimal spine end-to-end on a real mini-app first - `writing-the-contract` (+ oracles) -> `synthesizing-the-policy` -> `implementing-a-story` -> `verifying-against-contract` -> `adversarial-critic` -> `curating-the-ledger` (+ `ledger-check`) - one full loop working before expanding.
