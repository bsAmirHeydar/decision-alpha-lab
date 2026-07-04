# 11 — Hook Phase 04 Implementation: ND, Death Lifecycle, and X Closure Skeleton

## Phase Goal

Phase 04 adds lifecycle diagnostics to the CycleHook architecture:

```text
ND candidate
origin return penetration / death marker
X closure skeleton
50% retracement threshold
lifecycle state
CSV audit
```

This phase still does not add Hook Type A/B/C.

## Why This Phase Exists

Phase 02 created X sequences.

Phase 03 created Y opposite Extremes.

Phase 04 uses those objects to create a visible lifecycle skeleton before final type classification and full closure logic.

## Important Interpretation

This is still a skeleton.

It exposes lifecycle states and thresholds for audit.

It does not yet produce a trade signal and does not send orders.

## ND Candidate

Phase 04 treats ND as a return-toward-origin candidate.

Given the Phase 02 sequence definitions:

```text
Positive sequence:
    origin = valley
    X nodes = lower valleys
    return toward origin = upward

Negative sequence:
    origin = peak
    X nodes = higher peaks
    return toward origin = downward
```

The default ND threshold is 50% of the distance from the latest X node back toward origin.

## Death / Origin Return Penetration

Phase 04 draws a death/origin boundary at the origin price.

If the return goes through origin, the record is marked as:

```text
DEAD_BY_ORIGIN_RETURN
```

This is a lifecycle diagnostic.

## X Closure Skeleton

Phase 04 uses the latest available Y reference:

```text
Y01
Y12
Y23
Y34
```

For closure, the default requirement is:

```text
x_count >= 3
```

Then it calculates a 50% retracement threshold from the latest Y toward origin.

For positive Hook:

```text
Y is a high
closure = retrace downward from Y toward origin
```

For negative Hook:

```text
Y is a low
closure = retrace upward from Y toward origin
```

## Lifecycle States

```text
ALIVE
ND_CANDIDATE
X_CLOSURE_CANDIDATE
X_CLOSED
DEAD_BY_ORIGIN_RETURN
INSUFFICIENT_DATA
```

## Chart Objects

Phase 04 draws:

```text
ND marker
DEATH marker
X CLOSED marker
ND threshold
X closure threshold
origin / death boundary
lifecycle state labels
```

All objects use:

```text
DAL_HOOK_P04_
```

## CSV Outputs

If enabled:

```text
hook_phase04_lifecycle.csv
hook_phase04_summary.csv
```

## Deferred to Future Phases

Still deferred:

```text
Hook Type A/B/C
Y closure strength
XY closure
symmetry scoring
higher-level quality labels
training labels
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
