# 12 — Hook Phase 05 Implementation: Hook Type A/B/C Classifier

## Phase Goal

Phase 05 adds the Hook Type A/B/C classifier.

It uses the Y-axis opposite Extremes produced by Phase 03 and the lifecycle records produced by Phase 04.

This phase is still visualization and diagnostics only.

## Positive Hook Type Logic

For positive Hook:

```text
O   = origin valley
X1  = first lower valley
X2  = second lower valley
X3  = third lower valley
Y01 = high between O and X1
Y12 = high between X1 and X2
Y23 = high between X2 and X3
```

Type A:

```text
Y12 > Y01
and Y23 > Y12
```

Type B:

```text
Y12 > Y01
but Y23 does not exceed Y12
```

Type C:

```text
neither Type A nor Type B
```

## Negative Hook Type Logic

For negative Hook:

```text
O   = origin peak
X1  = first higher peak
X2  = second higher peak
X3  = third higher peak
Y01 = low between O and X1
Y12 = low between X1 and X2
Y23 = low between X2 and X3
```

Type A:

```text
Y12 < Y01
and Y23 < Y12
```

Type B:

```text
Y12 < Y01
but Y23 does not break Y12
```

Type C:

```text
neither Type A nor Type B
```

## Four-Node Handling

Phase 05 keeps the canonical classifier strict by default:

```text
Y01 / Y12 / Y23
```

An optional input allows using `Y34` as the third evidence if `Y23` is missing:

```text
InpHookPhase05AllowY34AsThirdEvidence
```

Default:

```text
false
```

This preserves the clean Type A/B/C logic.

## Classification Outputs

Each classified record includes:

```text
hook_type
type_state
condition_first
condition_second
confidence_score
type_rank_score
reason
```

Ranking:

```text
Type A = 3
Type B = 2
Type C = 1
Insufficient = 0
```

## Chart Objects

Phase 05 draws:

```text
HOOK A / HOOK B / HOOK C labels
type anchor marker
Y comparison lines
logic labels
```

All objects use:

```text
DAL_HOOK_P05_
```

## CSV Outputs

If enabled:

```text
hook_phase05_type_abc.csv
hook_phase05_summary.csv
```

## Deferred to Future Phases

Still deferred:

```text
symmetry scoring
quality scoring
XY closure strength
context/zone/entry labels
training labels
policy learning
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
