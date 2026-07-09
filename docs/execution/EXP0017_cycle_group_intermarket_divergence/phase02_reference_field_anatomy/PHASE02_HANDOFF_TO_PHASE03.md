# Phase 02 Handoff to Phase 03

Phase 03 should build Symbol Pair Data Anatomy on top of the Phase 01 and Phase 02 foundation.

## What Phase 03 receives

Phase 03 can rely on:

```text
same-day trading field
cycle-group registry
current cycle per CG
all completed previous cycles per CG
symbol-local reference high/low values
reference readiness state
M1 aggregation contract
```

## What Phase 03 must not change

Phase 03 must not change:

- the New York 18:00-17:00 trading-day boundary
- CG durations
- previous-cycle scope
- symbol-local reference doctrine
- M1 aggregation logic
- no-ranking-before-statistics doctrine

## Next practical objective

After Phase 02, the robot can be extended to understand each symbol's current-cycle high/low state relative to its own references.

That creates the data bridge needed for Phase 04 Hunt Anatomy.
