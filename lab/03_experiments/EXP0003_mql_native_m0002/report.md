# EXP0003 — M0002 Reversal/Continuation Exit Volatility

This experiment runs the M0002 central Expert Advisor. It reuses M0001 structural-node detection, territory math, log-range utilities, and reporting metrics, but uses M0001 completed-exit events with M0001 hunt/touch consumption filtering preserved. It then separates completed post-exit events into `REVERSAL_AFTER_EXIT` and `CONTINUATION_AFTER_EXIT` branches based on the node-side of the exit-completion candle.

Expected output prefixes:

```text
DAL_M0002_FINAL_AUDIT
DAL_M0002_FINAL_REVERSAL_AFTER_EXIT
DAL_M0002_FINAL_CONTINUATION_AFTER_EXIT
DAL_M0002_FINAL_REVERSAL_VS_CONTINUATION
```


## Logic repair v1.70

H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.
