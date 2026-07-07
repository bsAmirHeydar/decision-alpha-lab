# 09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder

## Phase Goal

Phase 02 turns the Phase 01 peak/valley node stream into actual CycleHook sequence candidates.

This is still not the full Hook engine.

Phase 02 builds:

```text
CycleHook sequence identity
positive / negative direction
origin
strict X nodes
death boundary marker at origin price
sequence state
chart sequence lines
CSV audit
```

It does not yet build:

```text
Y-axis opposite Extremes
ND state
closure logic
Hook Type A/B/C
symmetry scoring
training labels
execution logic
```

Those come in later phases.

## Integration Contract

The central expert receives a second Hook module:

```text
FP_HookPhase02Engine.mqh
```

Phase 02 uses the Phase 01 node source adapter internally and respects the same display family:

```text
RALLY_ONLY
HOOK_ONLY
RALLY_AND_HOOK
```

Default remains Rally-only, so existing F-counting behavior is preserved.

## Positive CycleHook Sequence

A positive Hook sequence starts from a valley and accepts strictly lower valley nodes.

```text
origin = valley
X1, X2, X3, X4 = strictly lower valleys
```

Equal lows are rejected because the strict node source and strict sequence rule do not accept equality.

## Negative CycleHook Sequence

A negative Hook sequence starts from a peak and accepts strictly higher peak nodes.

```text
origin = peak
X1, X2, X3, X4 = strictly higher peaks
```

Equal highs are rejected.

## Origin and Death Boundary

Phase 02 draws the death boundary at the origin price.

This is only a structural boundary marker in Phase 02.

Full death/ND lifecycle is intentionally deferred to a later phase so that sequence construction can be visually inspected first.

## Sequence States

Phase 02 defines:

```text
CANDIDATE
READY
MATURE
CAPPED
REJECTED
```

Interpretation:

```text
READY  = at least min_x_nodes_to_keep
MATURE = 3 or more X nodes
CAPPED = max_x_nodes_per_sequence reached
```

## Display Objects

Phase 02 can draw:

```text
origin marker
X node markers
X sequence lines
death boundary line
sequence labels
```

All objects are namespaced under:

```text
DAL_HOOK_P02_
```

## CSV Outputs

If enabled:

```text
hook_phase02_sequences.csv
hook_phase02_summary.csv
```

## No Execution Boundary

This phase does not add:

```text
OrderSend
OrderCheck
CTrade
broker requests
risk sizing
volume sizing
live trading behavior
```

## Phase 34 Correction — Seed-Owned Forward Sequence Builder

The current implementation must follow the seed-owned forward sequence doctrine. Phase 02 should no longer behave as a pure overlapping end-backward branch enumerator for the production Hook sequence view.

The corrected production behavior is:

1. collect same-side raw nodes in old-to-new order;
2. scope them inside an origin/death-boundary context;
3. choose the first raw node that has not participated in previous accepted sequences as `node 1`;
4. scan forward until the end of the raw list;
5. accept every strict adverse continuation as the next sequence number;
6. after a sequence is accepted, mark all its participating nodes as participated;
7. never allow a participated node to become `node 1` of a later overlapping sequence.

The guard is seed-only. It does not ban a participated node from being used as `2`, `3`, or `4` in a later valid sequence.

This correction was made because unrestricted branch enumeration can prematurely end sequences at `2` and then re-seed new sequences from internal nodes, creating noisy fractal recutting on the chart.

