# M0002 Hunt/Reject Document — Deprecated

This document is kept only as a historical note. The active M0002 module is not hunt/reject based.

Use:

```text
docs/operations/mql5_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md
```

Current logic: use exact M0001 completed-exit events with hunt/touch consumption preserved, classify the completed-exit candle close relative to `node_price`, and split the original M0001 event-window RTV into `REVERSAL_AFTER_EXIT` and `CONTINUATION_AFTER_EXIT`.


## Logic repair v1.70

H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.
