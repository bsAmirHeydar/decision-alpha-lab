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

The default M0002 metric is `EVENT_RTV`: classify each neutral completed-exit event by reversal/continuation, then measure the exact same event-window RTV semantics as M0001:

```text
mean_inside = mean log-range from entry through rtv_inside_end
mean_before = equal-length mean log-range before entry
RTV = mean_inside / mean_before
logRTV = log(RTV)
```

The final `exit_gap` outside-zone confirmation candles are excluded from the inside sample, exactly like M0001.

## Why M0002 has its own event builder

H0002 must not use M0001 hunt/touch/consume-filtered events directly as its sample, because M0001 can remove continuation cases before the branch split. H0002 uses the same node and territory math, but builds a neutral completed-exit sample: first territory touch, frozen event zone, strict `exit_gap` outside-zone completion, then close-vs-node classification.

## Implementation

```text
mql5/Experts/DecisionAlphaLab/M0002/M0002_ReversalContinuationExitVolatility.mq5
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Types.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Engine.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Reports.mqh
```
