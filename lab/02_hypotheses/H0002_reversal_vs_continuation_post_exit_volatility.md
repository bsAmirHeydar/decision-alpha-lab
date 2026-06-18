# H0002 — Reversal vs Continuation After Exit Volatility

## Hypothesis

After a structural-node territory event completes its strict exit-gap window, the completed event can be split into two node-side outcomes: reversal or continuation. The core question is whether the **same event-window RTV used in H0001** is concentrated more in reversal outcomes, continuation outcomes, or mixed across both.

## Branch definition

For LOW / valley nodes:

```text
exit-completion close above node_price => REVERSAL_AFTER_EXIT
exit-completion close below node_price => CONTINUATION_AFTER_EXIT
```

For HIGH / peak nodes:

```text
exit-completion close below node_price => REVERSAL_AFTER_EXIT
exit-completion close above node_price => CONTINUATION_AFTER_EXIT
```

This hypothesis is not based on a later hunt / non-hunt label. It is based only on the side of the node when the exit window completes.

## Primary measurement

The default M0002 metric is `EVENT_RTV`: classify each valid M0001 completed-exit event by reversal/continuation, then measure the exact same event-window RTV semantics as M0001:

```text
mean_inside = mean log-range from entry through rtv_inside_end
mean_before = equal-length mean log-range before entry
RTV = mean_inside / mean_before
logRTV = log(RTV)
```

The final `exit_gap` outside-zone confirmation candles are excluded from the inside sample, exactly like M0001.

## Why M0002 uses the M0001 event builder

H0002 must use the exact H0001/M0001 lifecycle as its sample. If M0001 consumes a node by hunt, or by touch when `CONSUME_BY_TOUCH` is selected, H0002 must not recycle that node into more reversal/continuation samples. If `CONSUME_BY_HUNT` is selected, a confirmed touch does not consume the node; the next cycle is recomputed exactly as in M0001 and can produce another valid H2 sample.

## Implementation

```text
mql5/Experts/DecisionAlphaLab/M0002/M0002_ReversalContinuationExitVolatility.mq5
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Types.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Engine.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Reports.mqh
```


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



## Logic repair v1.70 — exact H0001 consumption lifecycle

M0002 no longer builds its own neutral repeated exit stream. It calls `DAL_M0001ComputeEvents()` and labels valid touch-confirmed, RTV-ready M0001 events as reversal or continuation at the completed exit candle. Repeated touch-confirmed revisits are allowed only when M0001 itself allows them (`CONSUME_BY_HUNT`); they are not allowed after the node is actually consumed by the selected M0001 consume mode.


Runtime audit should print `consumeMode`, `touchCycle`, and `consumptionInputRespected=1` so the selected M0001 consumption lifecycle is visible in every H0002 run.
