---
id: contract-<feature-slug>          # e.g. contract-auth
version: 1                            # bump on every change; curator records a contract_version ledger entry
status: draft                         # draft | active | satisfied
stories: []                           # e.g. [story-12, story-13]; the stories this contract serves
---

<!--
  Authored by the ORACLE-AUTHOR, BLIND TO THE IMPLEMENTATION.
  Each acceptance criterion is paired with the cheapest reliable oracle that proves it,
  and every oracle MUST be run and watched FAIL (status: red) before any code exists.
  See episteme:writing-the-contract. Hands off to episteme:synthesizing-the-policy.
-->

# Contract: <feature name>

One or two sentences: what this feature lets a user/system do, and the force behind it. WHAT, not HOW.

## Acceptance criteria

<!--
  One observable behavior per AC (if it says "and", split it).
  oracle: the EXACT runnable check (named test case / command), not "the test suite".
          prefer the cheapest reliable gate: test > type-check > lint/grep > build > command.
          where no cheap oracle exists, use `oracle: manual: <exactly what to inspect>`.
  status: red until its oracle is watched failing for the RIGHT reason; flips to green only when the oracle passes.
-->

- AC-1: <human-readable criterion - an observable behavior>
  - oracle: `npm test -- <file>.spec.ts -t "<case name>"`
  - status: red
- AC-2: <human-readable criterion>
  - oracle: `tsc --noEmit`        # type/shape contract
  - status: red
- AC-3: <human-readable criterion>
  - oracle: `curl -s localhost:3000/health | jq -e '.ok == true'`   # HTTP surface
  - status: red

## Interfaces / surface

<!-- The public functions, endpoints, types, CLI flags this feature must expose. The contract names the surface; it does not dictate the internals. -->

- `<function/endpoint/type signature>`
- `<...>`

## Error taxonomy

<!-- The failure cases that MUST be handled. Give each its own oracle where a cheap one exists. -->

- `<ERROR_CODE / case>`: <when it occurs, how it surfaces (status code, error type, message)>
  - oracle: `npm test -- <file>.spec.ts -t "<error case>"`
  - status: red
- `<...>`

## Out of scope

<!-- Explicit non-goals. Load-bearing: this is what the adversarial critic uses to reject scope drift. At least one. -->

- <thing this feature deliberately does NOT do>
- <...>
