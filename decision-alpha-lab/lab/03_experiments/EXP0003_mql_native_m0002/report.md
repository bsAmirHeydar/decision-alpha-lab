# EXP0003 — M0002 Reversal/Continuation Exit Volatility

This experiment runs the M0002 central Expert Advisor. It reuses M0001 structural-node detection, territory math, log-range utilities, and reporting metrics, but builds a neutral completed-exit event sample without M0001 hunt/touch consumption filtering. It then separates completed post-exit events into `REVERSAL_AFTER_EXIT` and `CONTINUATION_AFTER_EXIT` branches based on the node-side of the exit-completion candle.

Expected output prefixes:

```text
DAL_M0002_FINAL_AUDIT
DAL_M0002_FINAL_REVERSAL_AFTER_EXIT
DAL_M0002_FINAL_CONTINUATION_AFTER_EXIT
DAL_M0002_FINAL_REVERSAL_VS_CONTINUATION
```
