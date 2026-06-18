# M0002 — Reversal vs Continuation After Exit Volatility

Version: 1.66

M0002 tests the second hypothesis in a separate MQL-native module. It reuses M0001 structural-node extraction, territory geometry, log-range math, random-baseline logic, and validation/reporting utilities. It uses the exact M0001 completed-event lifecycle; no separate neutral event stream is built.

## Central Expert Advisor

```text
mql5/Experts/DecisionAlphaLab/M0002/M0002_ReversalContinuationExitVolatility.mq5
```

`M0002_HuntRejectExitVolatility.mq5` remains only as a deprecated compatibility filename and now runs the same reversal/continuation logic.

## Include stack

```text
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Types.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Engine.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Reports.mqh
```

## Core hypothesis

After a structural-node territory touch has completed its strict `exit_gap` window outside the frozen event zone, the completed event is classified only by the completed-exit candle side relative to the original node price. The question is whether the **same M0001 event-window RTV** is more concentrated in reversal outcomes, continuation outcomes, or mixed across both.

This module does **not** classify by hunt / non-hunt and it does **not** discard candidate events because the node price was crossed before exit completion. The branch is decided immediately at the completed exit window.

## Event construction

H0002 must use M0001 finalized events as its research sample. If a node is consumed by H0001/M0001, no later reversal/continuation calculation is made for that node.

```text
1. Detect structural nodes with the same L-rule as M0001.
2. Use DAL_M0001ComputeEvents() to build the exact H0001 event stream.
3. Keep M0001 hunt priority, touch confirmation, exit_gap, consumption, revisit reset, warmup, and RTV semantics unchanged.
4. Only touch-confirmed, RTV-ready M0001 events enter H0002.
5. At the completed-exit candle, classify close vs node_price.
6. Measure the original M0001 event-window RTV by branch.
7. Once a node is consumed by M0001, H0002 produces no later events from that node.
```

## Branch rules

Let `outcome_index = exit_index + InpOutcomeCandleOffsetAfterExit`. Default is `0`, meaning the candle that completes the exit-gap confirmation window.

For LOW / valley nodes:

```text
close[outcome_index] > node_price => REVERSAL_AFTER_EXIT
close[outcome_index] < node_price => CONTINUATION_AFTER_EXIT
```

For HIGH / peak nodes:

```text
close[outcome_index] < node_price => REVERSAL_AFTER_EXIT
close[outcome_index] > node_price => CONTINUATION_AFTER_EXIT
```

If the close is exactly equal to the node price, the outcome is `UNKNOWN` and is excluded from branch measurement.

## Primary measurement window

Default measurement mode:

```text
InpMeasureMode = DAL_M0002_MEASURE_EVENT_RTV
```

In this mode, M0002 does **not** measure a new fixed window after the outcome candle. It measures the exact same event-window RTV used by H0001/M0001, then splits those completed events by the reversal/continuation label:

```text
eventRTV = mean(abs(log(high / low))) from event entry through rtv_inside_end
         / mean(abs(log(high / low))) over the equal-length pre-entry baseline

branchLog = log(eventRTV)
```

The final `exit_gap` outside-zone confirmation candles are excluded from the inside sample, exactly as in M0001. The branch label is an outcome classifier only; it must not change the measured event window.

## Optional diagnostic mode

Optional only:

```text
InpMeasureMode = DAL_M0002_MEASURE_POST_OUTCOME_FIXED
```

This measures a fixed future window after the outcome candle. It is useful for diagnostics, but it is not the primary H0002 metric.

## Inputs

```text
InpMeasureMode = DAL_M0002_MEASURE_EVENT_RTV
InpOutcomeCandleOffsetAfterExit = 0
InpPostOutcomeSampleBars = 20        # only used in POST_OUTCOME_FIXED mode
InpUseEventLengthForSample = false   # only used in POST_OUTCOME_FIXED mode
InpRandomSamplesPerEvent = 20
InpBrokerUtcOffsetHours = 0
InpRegimeLookbackBars = 100
```

Use `InpOutcomeCandleOffsetAfterExit=1` only if the research definition should classify using the first candle after the completed exit window, rather than the candle that completed the window.

## Reports

```text
DAL_M0002_FINAL_AUDIT
DAL_M0002_FINAL_REVERSAL_AFTER_EXIT
DAL_M0002_FINAL_REVERSAL_AFTER_EXIT_RANDOM
DAL_M0002_FINAL_REVERSAL_AFTER_EXIT_COMPARE
DAL_M0002_FINAL_REVERSAL_AFTER_EXIT_ROBUST
DAL_M0002_FINAL_REVERSAL_AFTER_EXIT_SESSION_REGIME
DAL_M0002_FINAL_CONTINUATION_AFTER_EXIT
DAL_M0002_FINAL_CONTINUATION_AFTER_EXIT_RANDOM
DAL_M0002_FINAL_CONTINUATION_AFTER_EXIT_COMPARE
DAL_M0002_FINAL_CONTINUATION_AFTER_EXIT_ROBUST
DAL_M0002_FINAL_CONTINUATION_AFTER_EXIT_SESSION_REGIME
DAL_M0002_FINAL_REVERSAL_VS_CONTINUATION
```

Positive `DAL_M0002_FINAL_REVERSAL_VS_CONTINUATION*dLogMean` means the M0001-native event RTV is higher in reversal outcomes. Negative means it is higher in continuation outcomes. Near zero means the volatility expansion is mixed rather than concentrated in one branch.


## v1.67 EVENT_RTV lock

H0002 is hard-locked to the native M0001 event RTV measurement window. Reversal/continuation is only a branch label assigned at the completed M0001 exit candle by comparing `close` with `node_price`. The branch label must not change the volatility window.

Expected audit markers:

```text
measureMode=EVENT_RTV
sampleWindow=m0001EventRtv
eventRtvMode=<paired_count>
postOutcomeMode=0
```

If an output still contains `sampleStarts=afterOutcomeCandle`, `sampleBars=20`, or `useEventLength=0` without `measureMode=EVENT_RTV`, it is from an old build and should not be used for H0002 conclusions.

## Deep audit repair notes

See `docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY.md` for the v1.69 audit. The key invariants are:

- exact H0001/M0001 hunt/touch consumption lifecycle before H2 classification;
- completed exit-gap candle close versus original node price is the only branch classifier;
- measured volatility is locked to M0001-native event RTV;
- random nulls use deterministic hash32 v2 uniform valid-entry sampling;
- each branch prints the full H1-style stress suite.



## Logic repair v1.70 — exact H0001 consumption lifecycle

M0002 no longer builds neutral repeated exit cycles. It calls `DAL_M0001ComputeEvents()` and only labels valid touch-confirmed, RTV-ready M0001 events as reversal or continuation at the completed exit candle. Once a node is consumed by the M0001 lifecycle, no further H0002 cycles are produced from that node.
