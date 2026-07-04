# 02 — CycleHook Object Model

## Canonical Rule

Hook and CycleHook are the same algorithmic object.

Recommended canonical object:

```text
CycleHook
```

## Directions

There are two directions:

```text
Positive CycleHook
Negative CycleHook
```

## Positive CycleHook

A positive CycleHook starts from a valley.

Its counted X nodes are valleys.

The sequence is strictly lower valleys.

Equal nodes are not accepted as new lower nodes.

```text
origin = valley
node sequence = strictly lower valleys
death = price penetrates origin
opposite Extreme = highest price between relevant valley nodes
ND = return toward origin without origin penetration
```

## Negative CycleHook

A negative CycleHook starts from a peak.

Its counted X nodes are peaks.

The sequence is strictly higher peaks.

Equal nodes are not accepted as new higher nodes.

```text
origin = peak
node sequence = strictly higher peaks
death = price penetrates origin
opposite Extreme = lowest price between relevant peak nodes
ND = return toward origin without origin penetration
```

## Death Rule

One-point penetration of the origin kills the CycleHook.

There is no structural buffer for validity.

Execution buffer may exist later, but structural validity is strict.

## Opposite Extreme

For a positive CycleHook, opposite Extremes are highs.

For a negative CycleHook, opposite Extremes are lows.

The opposite Extreme is used for:

```text
ND detection
Y-axis extraction
Hook Type A/B/C
projection / symmetry diagnostics
```

## Minimum L

L starts from 2.

L1 is not structurally meaningful for this Hook layer.

## CycleHook Fields

Suggested fields:

```text
cyclehook_id
direction
origin_node_id
origin_time
origin_price
current_state
death_boundary_price
node_count
x_node_ids
y_extreme_ids
opposite_extreme_price
nd_detected
closure_detected
hook_type
parent_cyclehook_id
scale_id
timeframe
```

## Lifecycle States

Suggested states:

```text
CYCLEHOOK_CANDIDATE
CYCLEHOOK_ALIVE
CYCLEHOOK_X_SEQUENCE_BUILDING
CYCLEHOOK_X_CLOSED
CYCLEHOOK_Y_SEQUENCE_BUILDING
CYCLEHOOK_XY_CLOSED
CYCLEHOOK_ND_ACTIVE
CYCLEHOOK_DEAD_BY_ORIGIN_PENETRATION
CYCLEHOOK_SUPERSEDED
CYCLEHOOK_HISTORICAL
```
