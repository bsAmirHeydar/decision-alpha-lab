# 10 — Hook Phase 03 Implementation: Y-Axis Opposite Extremes

## Phase Goal

Phase 03 adds the Y-axis layer to the CycleHook X-sequences produced by Phase 02.

The purpose is to make the opposite Extreme structure visible and auditable before implementing closure, ND, or Hook Type A/B/C.

## What Phase 03 Builds

For every valid Phase 02 sequence, Phase 03 extracts:

```text
Y01
Y12
Y23
Y34
```

These are the opposite Extremes between X boundaries.

## Positive CycleHook

For a positive Hook:

```text
origin = valley
X nodes = lower valleys
Y nodes = highest highs between X boundaries
```

Segments:

```text
Y01 = highest high between O and X1
Y12 = highest high between X1 and X2
Y23 = highest high between X2 and X3
Y34 = highest high between X3 and X4
```

## Negative CycleHook

For a negative Hook:

```text
origin = peak
X nodes = higher peaks
Y nodes = lowest lows between X boundaries
```

Segments:

```text
Y01 = lowest low between O and X1
Y12 = lowest low between X1 and X2
Y23 = lowest low between X2 and X3
Y34 = lowest low between X3 and X4
```

## Why This Is Separate

Closure and Hook Type A/B/C depend on Y-axis correctness.

Therefore, Y must be stabilized as its own phase before using it for decisions.

## Y States

Phase 03 defines:

```text
MISSING
PARTIAL
COMPLETE
```

`COMPLETE` means all available X segments have a corresponding Y extreme.

## Chart Objects

Phase 03 draws:

```text
Y extreme markers
Y labels
dashed Y lines
optional dotted X reference lines
Y state labels
```

All chart objects use the isolated prefix:

```text
DAL_HOOK_P03_
```

## CSV Outputs

If enabled:

```text
hook_phase03_y_axis.csv
hook_phase03_summary.csv
```

## Deferred to Future Phases

Still not included:

```text
ND detection
X closure
Y closure
XY closure
Hook Type A/B/C
symmetry
training labels
execution logic
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
