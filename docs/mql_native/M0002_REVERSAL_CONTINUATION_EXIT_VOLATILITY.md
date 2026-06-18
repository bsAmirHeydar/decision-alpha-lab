# M0002 — Reversal vs Continuation After Exit Volatility

Version: 1.64

M0002 tests the second hypothesis in a separate MQL-native module. It reuses M0001 structural-node extraction, territory geometry, log-range math, and validation/reporting utilities, but it now builds its own neutral completed-exit events so hunt/touch consumption cannot pre-filter reversal or continuation outcomes.

## Central Expert Advisor

```text
mql5/Experts/DecisionAlphaLab/M0002/M0002_ReversalContinuationExitVolatility.mq5
```

## Include stack

```text
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Types.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Engine.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Reports.mqh
```

## Core hypothesis

After a structural-node territory touch has completed its strict `exit_gap` window outside the frozen event zone, the next state is classified only by the completed-exit candle side relative to the original node price. The question is whether post-exit volatility expansion is concentrated more in reversal branches, continuation branches, or mixed across both.

This module does **not** classify by later hunt / non-hunt and it does **not** discard candidate events because the node price was crossed before exit completion. The branch is decided immediately at the completed exit window.

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

## Measurement window

The branch volatility sample starts after the classification candle:

```text
sample_start = outcome_index + 1
```

The measured branch RTV is:

```text
branchRTV = mean(abs(log(high / low))) over post-outcome sample / mean(abs(log(high / low))) over pre-entry baseline
branchLog = log(branchRTV)
```

The baseline is still before the original event entry:

```text
baseline_start = entry_index - sample_length
```

This preserves the same anti-lookahead principle as M0001.

## Inputs

```text
InpOutcomeCandleOffsetAfterExit = 0
InpPostOutcomeSampleBars = 20
InpUseEventLengthForSample = false
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

Positive `DAL_M0002_FINAL_REVERSAL_VS_CONTINUATION*dLogMean` means the reversal branch is more volatile than the continuation branch. Negative means continuation is more volatile. Near zero means the volatility expansion is mixed rather than concentrated in one branch.

## Logic lock

M0002 keeps M0001 unchanged, but does **not** consume M0001 finalized/touch-confirmed events as its research sample. That caused selection bias because M0001 hunt/consume semantics can remove continuation candidates before branch classification.

M0002 now builds neutral completed-exit events:

```text
1. Detect structural nodes with the same L-rule as M0001.
2. Build live/frozen territories with the same M0001 territory formula.
3. Start an event at the first candle that intersects the live territory.
4. Freeze that event zone.
5. Ignore hunt/touch consumption while the event is pending.
6. Wait for exit_gap consecutive candles fully outside the frozen event zone.
7. At the completed-exit candle, classify close vs node_price.
8. Measure future post-outcome volatility by branch.
```

Only after this neutral exit-completion sample is built does M0002 run reversal/continuation statistics and random baselines.


## Compatibility filename

`M0002_HuntRejectExitVolatility.mq5` is kept as a deprecated compatibility entry point only. It now contains the same neutral exit reversal/continuation logic as `M0002_ReversalContinuationExitVolatility.mq5` so old MetaEditor tabs do not fail with removed hunt/reject input names. Prefer compiling `M0002_ReversalContinuationExitVolatility.mq5`.
