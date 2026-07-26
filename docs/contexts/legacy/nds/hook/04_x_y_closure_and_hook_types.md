# 04 — X/Y Closure and Hook Types

## X-Axis

The X-axis is the primary counted node sequence.

Positive X-axis:

```text
descending valleys
```

Negative X-axis:

```text
ascending peaks
```

X closure is usually the minimum reversal-power requirement.

## Y-Axis

The Y-axis is built from opposite Extremes between the X nodes.

Positive CycleHook Y-axis:

```text
opposite highs between valley nodes
```

Negative CycleHook Y-axis:

```text
opposite lows between peak nodes
```

Y gives zone precision and momentary energy.

## XY Closure

When both X and Y structure close, the reversal case is stronger.

Suggested labels:

```text
X_ONLY_CLOSED
Y_ONLY_CLOSED
XY_CLOSED
```

## Closure Rule

A Hook can be treated as closed when:

```text
sequence reaches 3 or 4 nodes
and price retraces more than 50% from opposite Extreme toward origin
```

Symmetry is not required for closure.

Symmetry is used for projection, zones, ND, and entry precision.

## ND

ND is the return toward origin without origin penetration.

ND is not death.

Death happens only when origin is penetrated.

## Hook Type A/B/C — Positive

Given:

```text
O   = origin valley
N1  = first lower valley
N2  = second lower valley
N3  = third lower valley
E01 = high between O and N1
E12 = high between N1 and N2
E23 = high between N2 and N3
```

Type A:

```text
E12 > E01
and E23 > E12
```

Type B:

```text
E12 > E01
but E23 does not exceed E12
```

Type C:

```text
neither Type A nor Type B
```

Positive ranking:

```text
A strongest
B middle
C weakest
```

## Hook Type A/B/C — Negative

Invert the logic.

Given opposite lows:

```text
E01 = low between O and N1
E12 = low between N1 and N2
E23 = low between N2 and N3
```

Type A negative:

```text
E12 < E01
and E23 < E12
```

Type B negative:

```text
E12 < E01
but E23 does not break E12
```

Type C negative:

```text
neither Type A nor Type B
```

## Four-Node Handling

Four-node classification should be structure-based and approximate.

Do not force a strict sliding-window rule if it conflicts with NDS structure.

Suggested priority:

```text
try Type A
then Type B
then Type C
allow down-weighting or ignoring a confusing node
```

## Fields

Suggested fields:

```text
x_closed
y_closed
xy_closed
closure_bar
closure_price
retracement_percent
nd_active
death_detected
hook_type
hook_type_confidence
hook_type_reason
symmetry_score
```
