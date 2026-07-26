---
tags: [exp0019, faerie-protocol, fp-i08, weekly-context, acceptance]
status: normative
phase: FP-I08
version: 1.0.0
last_updated: 2026-07-13
language: en
---
# FP-I08 Acceptance Gate

## Acceptance decision

The Python implementation, closed contracts, authority boundary, golden vectors, MQL5 static
surface, release inventory, and clean-baseline patch replay must all pass before FP-I08 may be
handed to FP-I09. Actual MetaEditor compilation remains a mandatory local Windows gate.

## Required semantic checks

1. The compiler uses the previous completed `W` window as reference and the current `W` window as check.
2. Weekly High and Low plans preserve symbol-local reference identity and price.
3. M1 first-sweep classification is delegated to FP-I06.
4. Closed-host-candle confirmation is delegated to FP-I07.
5. Double hunt cannot produce an active WW context.
6. Only a post-confirmation protected-symbol touch of the matching weekly side/reference neutralizes WW.
7. Contexts expire at the end of their check week if still confirmed.
8. The newest active confirmed context wins without deleting older contexts.
9. No active WW with complete data allows both directions.
10. Incomplete weekly data blocks downstream eligibility.
11. An opposing downstream signal is retained with `SUPPRESSED`, not removed.
12. A WW signal is directly tradeable and is not recursively suppressed by its own gate.

## Executed evidence in the supplied archive

- FP-I08 phase tests: `47 passed`.
- Available cumulative FP-I02 through FP-I08 tests: `420 passed`.
- All 15 JSON Schemas are closed Draft 2020-12 object schemas.
- Boundary and MQL5 static checks pass inside the phase suite.
- The supplied base archive does not contain the exact pinned shared-core directories required
  by the historical FP-I00/FP-I01 compatibility gates, and it does not contain the EXP0018 Daye
  regression tree. Those upstream suites are therefore recorded as unavailable in this build
  environment, not represented as passing.
- Actual MetaEditor compilation: `pending_local_windows`.

## Release rule

FP-I09 may consume the contracts after the local MetaEditor gate. Live execution remains blocked
by unresolved `FP-DEC-012` regardless of FP-I08 status.

## Navigation

- [[00_FP_I08_DELIVERY_MOC|FP-I08 Delivery MOC]]
- [[35_TEST_STRATEGY|Test Strategy]]
- [[41_RELEASE_AND_ROLLBACK|Release and Rollback]]
- [[43_HANDOFF_TO_FP_I09|FP-I09 Handoff]]
