# H0002 — Reversal vs Continuation After Exit Volatility

## Hypothesis

After a structural-node territory event completes its strict exit-gap window, future volatility may concentrate differently depending on whether price has reversed away from the original node side or continued through the original node side.

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

This hypothesis is not based on a later hunt / non-hunt label. It is based only on the side of the node after the exit window completes.

## Main question

Is future logRTV after the completed event more concentrated in the reversal branch, more concentrated in the continuation branch, or mixed across both?

## Implementation

```text
mql5/Experts/DecisionAlphaLab/M0002/M0002_ReversalContinuationExitVolatility.mq5
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Types.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Engine.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Reports.mqh
```

## Event construction rule

H0002 must not use M0001 finalized/touch-confirmed events directly as its sample, because M0001 hunt/consume logic can filter out continuation cases before the reversal/continuation split. H0002 uses the same node and territory math, but builds a neutral completed-exit sample: first territory touch, frozen event zone, strict `exit_gap` outside-zone completion, then close-vs-node classification.
