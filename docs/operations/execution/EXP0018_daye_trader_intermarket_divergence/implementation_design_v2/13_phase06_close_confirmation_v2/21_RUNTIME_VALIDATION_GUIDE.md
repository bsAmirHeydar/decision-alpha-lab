---
id: EXP0018-P06-RUNTIME
title: "P06 Runtime Validation Guide"
type: implementation-note
status: implemented
project: EXP0018
phase: P06
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - p06
  - confirmation
---

# Runtime validation

1. Compile with zero errors and zero warnings.
2. Verify embedded P05 and P06 self-tests pass.
3. Run on M1 and M30 charts separately.
4. Observe source baseline without immediate retroactive candidates.
5. Produce a live one-sided transition.
6. Verify exactly one target host close is assigned.
7. Verify BOTH before close invalidates.
8. Restart before close and verify checkpoint restoration.
9. Delay the terminal across a host close and verify replay-required fail-closed behavior.
10. Confirm no chart objects or orders are created.
