# Phase 04 Handoff To Phase 05

Phase 05 should build the confirmation and invalidation boundary.

## Inputs provided by Phase 04

```text
raw divergence candidates
candidate direction
candidate side
hunter symbol
clean symbol
reference cycle
current cycle
clean stop reference preview
symmetric no-divergence counts
missing-data exclusions
```

## Phase 05 must add

```text
active chart timeframe candle close boundary
confirmed divergence state
tradeable-signal state
final confirmation time
double-hunt invalidation at confirmation
post-confirmation invalidation observation
candidate lifecycle state
```

## Constraint

Phase 05 must not change the definition of high-side sell divergence or low-side buy divergence. It may only determine whether the candidate survives to confirmed/tradeable status.
