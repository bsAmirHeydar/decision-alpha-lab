# M0002 Hunt/Reject Document — Deprecated

This document is kept only as a historical note. The active M0002 module is not hunt/reject based.

Use:

```text
docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md
```

Current logic: build neutral completed-exit events without hunt/touch filtering, classify the completed-exit candle close relative to `node_price`, and split the original M0001 event-window RTV into `REVERSAL_AFTER_EXIT` and `CONTINUATION_AFTER_EXIT`.
