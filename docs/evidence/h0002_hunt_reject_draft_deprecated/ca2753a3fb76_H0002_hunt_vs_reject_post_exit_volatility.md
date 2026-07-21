# H0002 Hunt/Reject Draft — Deprecated

This draft is kept only for history. It is not the active H0002 definition.

The active hypothesis is:

```text
lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility.md
```

The active implementation is:

```text
mql5/Experts/DecisionAlphaLab/M0002/M0002_ReversalContinuationExitVolatility.mq5
```

Reason for deprecation: the second hypothesis is not a hunt/non-hunt split. It is a M0001 completed-exit branch split by the completed-exit candle close relative to the original node price, with the primary metric equal to the same M0001 event-window RTV split by branch.


## Logic repair v1.70

H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.
