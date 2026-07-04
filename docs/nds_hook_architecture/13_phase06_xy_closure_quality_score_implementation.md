# 13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score

## Phase Goal

Phase 06 adds an independent X/Y closure-strength and structural quality layer on top of Phase 05.

It uses:

```text
Phase 03 Y-axis opposite Extremes
Phase 04 lifecycle / ND / death / X closure records
Phase 05 Hook Type A/B/C classification
```

This phase is still visualization and diagnostics only.

## Why This Phase Exists

Hook Type A/B/C is a global structural classifier.

X/Y closure quality is a different layer:

```text
Hook type = broader whole-Hook shape
X closure = return/closure state from Phase 04 lifecycle
Y closure = internal Y-sequence step behavior
quality score = combined structural audit score
```

This separation is required because a Hook can be Type A/B/C while still having weak or incomplete internal X/Y closure.

## Y-Sequence Closure Logic

For positive CycleHook:

```text
X = descending valleys
Y = opposite highs between X nodes
Y-sequence closure expects opposite highs to step lower
```

Positive Y checks:

```text
Y12 < Y01
Y23 < Y12
Y34 < Y23
```

For negative CycleHook:

```text
X = ascending peaks
Y = opposite lows between X nodes
Y-sequence closure expects opposite lows to step higher
```

Negative Y checks:

```text
Y12 > Y01
Y23 > Y12
Y34 > Y23
```

This is intentionally different from Hook Type A/B/C logic.

## X Closure Input

Phase 06 reads the Phase 04 lifecycle fields:

```text
x_closure_candidate
x_closed
nd_detected
origin_return_penetrated
lifecycle_state
```

Default policy:

```text
InpHookPhase06RequireXClosedForXY = true
```

So `XY_CLOSED` requires real Phase 04 `x_closed`, not just a candidate.

## XY Closure States

Phase 06 emits:

```text
OPEN
X_ONLY
Y_ONLY
XY_CLOSED
DEAD_BY_ORIGIN_RETURN
INSUFFICIENT
```

Meaning:

```text
OPEN       = neither X nor Y closure is complete
X_ONLY     = X closure exists without Y-sequence closure
Y_ONLY     = Y-sequence closure exists without X closure
XY_CLOSED  = both X and Y are closed
DEAD       = origin-return penetration killed the CycleHook role
INSUFFICIENT = missing required X or Y evidence
```

## Quality Score

Phase 06 computes:

```text
x_strength
y_strength
type_strength
lifecycle_strength
quality_score
quality_bucket
```

Default weights:

```text
x_weight         = 0.30
y_weight         = 0.30
type_weight      = 0.20
lifecycle_weight = 0.20
```

Default buckets:

```text
ELITE  >= 0.80
HIGH   >= 0.65
MEDIUM >= 0.45
LOW    >= 0.25
INVALID otherwise, or dead/insufficient
```

## New MQL5 Modules

```text
FP_HookPhase06Types.mqh
FP_HookPhase06Rules.mqh
FP_HookPhase06Visual.mqh
FP_HookPhase06Export.mqh
FP_HookPhase06Engine.mqh
```

## New Expert Inputs

```text
InpHookPhase06Enabled
InpHookPhase06ShowPositive
InpHookPhase06ShowNegative
InpHookPhase06DrawQualityLabel
InpHookPhase06DrawXYAnchor
InpHookPhase06DrawProjectionLines
InpHookPhase06DrawLabels
InpHookPhase06ExportCsv
InpHookPhase06PrintSummary
InpHookPhase06PrintSamples
InpHookPhase06IncludeDeadRecords
InpHookPhase06RequireXClosedForXY
InpHookPhase06MinXNodesForQuality
InpHookPhase06MinYComparisonsForClosed
InpHookPhase06XWeight
InpHookPhase06YWeight
InpHookPhase06TypeWeight
InpHookPhase06LifecycleWeight
InpHookPhase06EliteThreshold
InpHookPhase06HighThreshold
InpHookPhase06MediumThreshold
InpHookPhase06LowThreshold
```

## Chart Objects

Phase 06 draws objects with:

```text
DAL_HOOK_P06_
```

Objects include:

```text
XY anchor
quality label
Y-step projection lines
logic label
```

## CSV Outputs

If enabled:

```text
hook_phase06_xy_quality.csv
hook_phase06_summary.csv
```

The row-level CSV includes:

```text
sequence_id
direction
scale_l
hook_type
lifecycle_state
y_state
xy_state
quality_bucket
quality_score
x_strength
y_strength
type_strength
lifecycle_strength
Y comparison booleans
anchor slot/time/price
reason
```

## Preservation Rules

Default display family remains:

```text
FP_NDS_HOOK_DISPLAY_RALLY_ONLY
```

So Rally/F-counting behavior remains unchanged unless the operator explicitly selects Hook-only or Rally-and-Hook.

## Deferred to Later Phases

Still deferred:

```text
symmetry projection
adaptive ND thresholding
adaptive Extreme width
context/zone/entry labeling
AI training labels
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
