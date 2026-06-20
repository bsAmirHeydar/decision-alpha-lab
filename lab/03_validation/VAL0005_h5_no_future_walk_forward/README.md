# VAL0005 — H5 No-Future Walk-Forward Validation

Validation target: H0005 must be evaluated exactly as it would be available live.

## Rule

H5 must not be validated by building a complete historical array once and then asking earlier candles what the future-completed node/regime was. The validation process must advance one candle at a time.

## Implementation

Use:

```text
mql5/Experts/DecisionAlphaLab/Debug/D0005_H5NoFutureWalkForwardAudit.mq5
```

The debugger replays history using prefix-only bar arrays. At each cursor candle it reconstructs:

1. M0001 structural nodes
2. M0001 events
3. M0002 latest branch regime

The result is the regime that would have existed live at that candle.

## Pass condition

Primary pass condition:

```text
futureViolationSteps = 0
```

Secondary sanity conditions:

```text
okSteps > 0
reversalSteps + continuationSteps > 0
```

## Why this matters

Structural nodes need right-side confirmation. If a historical report treats a pivot node as known at the pivot candle instead of at its confirmation candle, the report is using future information. That makes the H5 result look cleaner than live trading can actually reproduce.

This validation forces the algorithm to respect node availability time through `active_from_index` and prefix-only data loading.
