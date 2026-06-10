# Episteme

**An epistemic control layer for agentic software development.**

> "Done" is *proven against a contract* by a cheap oracle and an independent critic -
> never *declared* by the implementer.

Episteme is a portable skills + tools package (a Claude Code plugin) that wraps
your coding agent in one mandatory loop:

```
contract  ->  gated policy  ->  implement  <->  verify  ->  adversarial critic  ->  curate ledger
```

It is the layer that BMAD, Superpowers, and harnesses like Pi each *gesture* at but
none enforce as a spine. This flow is **Metis** -
**M**ulti-agent **E**pistemic **T**yped-ledger **I**nvestigation **S**ynthesis - the
reasoning architecture Episteme runs on, distilled from our `world_model_v2`
ARC-AGI-3 research agent. Episteme is the framework; **Metis is the architecture it
powers** (full spec in [docs/METIS.md](docs/METIS.md)).

## Why (beyond BMAD / Superpowers)

BMAD gives you a full spec-driven lifecycle; Superpowers gives you execution
discipline (TDD, verification-before-completion); Pi gives you a typed session
ledger. Each is excellent. What none makes *mandatory and woven* is the epistemic
control: a verifiable contract, a typed curated memory with authority, an
adversarial critic that reads the contract (not your code), and a cheap-oracle gate
on every claim. Episteme is exactly that control layer - and it interoperates with,
rather than replaces, the workflow tools (it credits all of them; see Lineage).

## Install (Claude Code)

```
/plugin marketplace add <owner>/episteme
/plugin install episteme@episteme
# restart Claude Code
```

The deterministic validators need Python 3 plus one package: `pip install jsonschema`.

A SessionStart hook then injects the `using-episteme` bootstrap so the agent knows it
has Episteme. Verify install-readiness any time with `python3 tools/plugin-check.py`.

## Quickstart

Ask your agent for a real feature and tell it to use Episteme:

> "Build a CSV export endpoint for the report page - use `episteme:develop`."

The loop will: write `.episteme/contract.md` (each acceptance criterion paired with a
failing test, authored before any code) -> synthesize a gated plan -> implement one
change at a time -> run the oracle after every change -> have an independent critic
audit the diff against the contract -> record decisions in `.episteme/ledger.jsonl`.
"Done" means: every oracle green, critic approve, ledger-check clean. This repo's own
`.episteme/` directory is a real run of exactly that loop (the framework was built
with itself - see [Status](#status)).

## Usage

Invoke the orchestrator for any real feature:

- **`episteme:develop`** picks a track:
  - **Quick** (mini-app / single feature): straight to the loop on one `contract.md`.
  - **Full** (greenfield / large): `brief -> PRD -> architecture -> stories`, then the loop per story.

Or invoke any single voice directly (e.g. `episteme:adversarial-critic` to audit an
existing diff against a contract). All runtime artifacts live in `.episteme/`.

## The skills (14)

- **Orchestrator:** `develop` ; **Bootstrap:** `using-episteme`
- **The loop's voices:** `writing-the-contract`, `synthesizing-the-policy`,
  `implementing-a-story`, `verifying-against-contract`, `adversarial-critic`,
  `curating-the-ledger`
- **Full-track lifecycle:** `writing-a-brief`, `writing-a-prd`,
  `deciding-architecture`, `sharding-into-stories`, `writing-a-story`
- **Meta:** `writing-episteme-skills` (how to author new skills that fit the loop)

## The tools (deterministic oracles)

`ledger.jsonl`, `policy.json`, `verdict.json`, and the PRD->ledger through-line each
have a cheap deterministic validator (Pillar 4 in action - lean on cheap gates):

- `tools/ledger-check.py` - typed memory integrity (schema + unique ids + supersedes chain)
- `tools/policy-check.py` - policy shape + the readiness gate (a `ready` policy may only rest on `verified` ledger entries)
- `tools/verdict-check.py` - verdict shape
- `tools/prd-check.py` - every PRD Assumptions-Index ref is a ledgered assumption
- `tools/plugin-check.py` - install-readiness (manifest, skills, hook)

Schemas in `schemas/` are the single source of truth, shared with a future Pi
(TypeScript) extension.

## The four pillars

1. **Contract-as-truth** - the contract, not the agent's word, defines done; the
   verifier and critic read it.
2. **Curated ledger** - typed memory (`.episteme/ledger.jsonl`) with source +
   authority (`verified` vs `assumed`); a hypothesis never silently becomes a fact.
3. **Adversarial verification with epistemic separation** - the oracle/test author
   writes tests from the contract blind to the implementation; a separate post-diff
   critic audits compliance, drift, and architecture.
4. **Right-oracle doctrine** - lean on cheap deterministic gates (tests, types,
   lint, build, the validators above); reserve LLM judgment for where no cheap
   oracle exists.

## Lineage (credited, not hidden)

Episteme is an original control layer, not a fork. It stands on and interoperates
with **BMAD** (the SDD lifecycle scaffolding), **Superpowers** (the skills-as-files
model + execution discipline), and **Pi** (the typed session ledger primitive) - all
MIT. The contribution that is ours is binding contract + typed ledger + gated policy +
factual verifier + adversarial critic into one *mandatory* loop, distilled from
deep agent R&D (internally, "Metis").

## Status

v0.1. The loop is validated end-to-end by dogfood: both the Quick track and the Full
track (`brief -> PRD -> architecture -> stories -> loop`, including a spike) were run
to build Episteme's own validators, with every Iron-Law gate green. Not yet
battle-tested across diverse external repos.

## Read more

- [docs/CONSTITUTION.md](docs/CONSTITUTION.md) - the thesis: the four pillars, the gaps in BMAD/Superpowers/Pi, the lineage.
- [docs/METIS.md](docs/METIS.md) - the architecture spec, voice by voice.
- [docs/SCAFFOLD_PROPOSAL.md](docs/SCAFFOLD_PROPOSAL.md) - the pre-build design record.

## License

MIT - see [LICENSE](LICENSE).
