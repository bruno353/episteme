---
id: corpus-<slice-id>                 # e.g. corpus-billing-calc
slice: <slice-id>                     # the migration slice this corpus characterizes
status: capturing                     # capturing | frozen | stale
captured_from: <legacy system + env>  # e.g. "legacy batch engine, prod replica, build 4.2"
captured_at: <date or date range>     # when the recordings were taken
entries: 0                            # exact entry count; verifier checks this every replay
content_hash: <sha256 of the canonical corpus archive>   # verifier checks this every replay
replay_command: <exact command>       # the oracle the contract's equivalence ACs declare
---

<!--
  Assembled when the slice contract is authored (episteme:writing-the-contract);
  read-only afterwards - episteme:verifying-equivalence checks the content hash
  every replay. The manifest exists to make the Iron Law mechanically checkable:
  EXPECTED OUTPUTS COME FROM THE LEGACY CAPTURE, NEVER FROM THE NEW CODE.
  entries + content_hash pin the capture; any change outside an adjudication record
  is tampering and fails verification (verdict kind=mismatch, reason naming the
  tampering; corpus flagged suspect - develop's "Oracle integrity" doctrine).
  Expected outputs are NEVER edited inline - overrides live in .episteme/parity-map.md
  (episteme:adjudicating-parity, par-NNNN) and are only POINTED TO from here.
-->

# Corpus manifest: <slice name>

One or two sentences: what behavior this corpus captures (inputs -> outputs of which
legacy surface), and what triggered the capture.

## Provenance

<!-- Enough detail that someone could re-capture from LEGACY (never from the new system). -->

- Source surface: <endpoint / batch job / function boundary recorded>
- Capture method: <proxy tap, log extraction, instrumented run, db snapshot diff>
- Input population: <real traffic window? sampled? hand-picked edge cases?>

## Coverage (facts, then gaps)

<!-- The verifier reports counts; sufficiency is judged here and by the critic/adjudicator.
     A green replay on a thin corpus is a thin green - say what is thin. -->

- Covered: <input regions / branches the entries exercise, with counts>
- Known gaps: <input regions NOT represented; each gap is a risk the cutover gate inherits>

## Normalization rules (the ONLY fields excluded from equivalence)

<!--
  Each rule is an adjudicated decision about meaning, with a reason and a decider.
  The verifier applies EXACTLY these rules - never one invented mid-turn to turn a
  red entry green (that is editing the expected output through a side door).
-->

| rule | field/pattern | why it is not part of equivalence | decided by | date |
|---|---|---|---|---|
| norm-1 | `response.timestamp` | wall-clock, regenerated per run | <who> | <date> |

## Adjudicated overrides (pointers only - the capture is never edited)

<!-- One row per corpus entry whose EXPECTED is overridden by a parity-map adjudication
     (category (c): legacy bug, adjudicated as fix). The override content lives in the
     parity-map record, not here. Preserve decisions (category (b)) need no row - the
     capture already IS the expected. -->

| entry | parity-map ref | decision | decided by | date |
|---|---|---|---|---|
| <entry-id> | par-NNNN | fix (expected overridden) | <who> | <date> |

## Freshness / staleness triggers

<!-- When does this corpus stop being trustworthy testimony? Name the triggers. -->

- Stale if: <legacy system patched after captured_at; upstream schema change; a
  parallel-run divergence reveals an input class the corpus misses>
- On stale: re-capture from legacy (bump version, new content_hash); never refresh
  from the new system.
