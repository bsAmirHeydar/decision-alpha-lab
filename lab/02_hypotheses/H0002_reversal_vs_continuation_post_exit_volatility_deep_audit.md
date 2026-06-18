# H0002 Deep Audit

H0002 splits completed neutral exit events into reversal and continuation branches by close versus the original node price at the completed exit candle.

It must not filter by hunt/touch outcome before classification. It must not measure a separate post-outcome fixed window by default. The branch label splits the same M0001 event RTV.

Primary evidence lines:

```text
DAL_M0002_BUILD_SANITY
DAL_M0002_FINAL_AUDIT
DAL_M0002_FINAL_RANDOM_ENGINE_AUDIT
DAL_M0002_FINAL_REVERSAL_AFTER_EXIT_COMPARE
DAL_M0002_FINAL_CONTINUATION_AFTER_EXIT_COMPARE
DAL_M0002_FINAL_REVERSAL_VS_CONTINUATION
```

Full stability lines for each branch:

```text
*_STRESS_NULLS
*_PLACEBO
*_OUTLIER_STRESS
*_NONOVERLAP
*_CLUSTER_ROBUST
*_BLOCK_BOOT
*_HORIZON
*_NEGATIVE_CONTROL
```
