---
# Adversarial-critic verdict (Voice 3, post-diff). One per audited diff/approach.
# Authored by the `episteme:adversarial-critic` skill. The critic reads
# contract.md + .episteme/ledger.jsonl + the DIFF + the verifier's verdicts -
# NEVER the implementer's private reasoning.
contract: contract-<feature-slug>        # which contract was audited
audited_at_turn: <int>                    # loop turn index (freshness)
diff_ref: <commit-sha | branch | patch-id># what diff/approach this verdict covers
verdict: approve | reject                 # default-approve; reject ONLY with cited evidence
contradiction_type: null                  # null on approve; on reject a short label, e.g.
                                          # compliance_gap | scope_creep | out_of_scope_edit
                                          # | constraint_violation | future_step_script_leak
---

# Critic report: <feature name>

## Verdict

**<approve | reject>**

## Reasoning

<2-3 sentences. Name which of the 3 audit axes failed (or "all axes clear"):
 (1) contract compliance, (2) drift / scope creep, (3) architecture.>

## Axis findings

- **Axis 1 - contract compliance:** <pass | fail + one line> <every AC's oracle green AND intent satisfied?>
- **Axis 2 - drift / scope creep:** <pass | fail + one line> <anything outside scope / on the Out-of-scope list?>
- **Axis 3 - architecture:** <pass | fail + one line> <any `verified` constraint violated? future-step script leak?>

## Cited contract items

<!-- The AC-N / contract sections this verdict references. Empty on a clean approve. -->
- <AC-N: criterion text> (e.g. "AC-3: rejects expired token")

## Cited evidence

<!-- Ledger ids and file:line references that ground the verdict. Empty on a clean approve.
     A reject with NO cited evidence is invalid - downgrade to approve. -->
- <led-XXXX: constraint statement> (must be a `verified` entry to ground a reject)
- <path/to/file.ts:NN-MM: what is at that line>

## Suggested fix

<!-- Required on reject, optional on approve. Direct the author/curator at what to
     RECONSIDER - never a replacement implementation. The critic judges, it does not author. -->
<e.g. "Reconsider whether the diff satisfies AC-3's intent: the oracle is green but
 only exercises the happy path; the criterion requires the expired-token case.">

## Items to revisit (handoff to the curator)

<!-- On reject: the ledger entries / contract sections the curator must reconsider
     before the implementer retries. Also where an `assumed` entry the diff contradicts
     goes (it is NOT a hard-reject reason - the curator reconciles it). Empty on a clean approve. -->
- <led-XXXX: what the curator should reconsider, and why (which axis / which new fact)>

## Force-approve caveat

<!-- Present ONLY when the anti-deadlock cap forced this approve (3rd consecutive
     same-signature rejection). Delete this whole section otherwise. -->
<!--
force_approved: true
unresolved_signature: <axis + cited items that was rejected 2x>
note: "Force-approved after 2 rejections of the above signature; the cited concern was
 NOT resolved. The loop must not deadlock - the concern is now the curator's to carry
 as items_to_revisit. This approve does NOT mean the concern was answered."
-->
