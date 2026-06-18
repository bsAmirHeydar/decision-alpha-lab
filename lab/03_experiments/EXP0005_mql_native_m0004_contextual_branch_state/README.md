# EXP0005 — MQL-native contextual branch-state diagnostics

Run `M0004_BranchRegimeClustering.mq5` build 1.02 and inspect the contextual report lines.

Required lines:

```text
DAL_M0004_FINAL_CONTEXT_LAST_ONLY_REFERENCE
DAL_M0004_FINAL_CONTEXT_ROLLING_FAST
DAL_M0004_FINAL_CONTEXT_ROLLING_MAIN
DAL_M0004_FINAL_CONTEXT_ROLLING_SLOW
DAL_M0004_FINAL_CONTEXT_EWMA_MAIN
DAL_M0004_FINAL_CONTEXT_BUCKETS_ROLLING_MAIN
DAL_M0004_FINAL_CONTEXT_BUCKETS_EWMA_MAIN
DAL_M0004_FINAL_CONTEXT_SHUFFLE_STRESS_ROLLING
DAL_M0004_FINAL_CONTEXT_STRATIFIED_STRESS_ROLLING
DAL_M0004_FINAL_CONTEXT_SHUFFLE_STRESS_EWMA
DAL_M0004_FINAL_CONTEXT_STRATIFIED_STRESS_EWMA
```

Interpretation priority:

1. `dominantLiftPct` should be positive.
2. `conflictContextMinusLastPct` tells whether context beats last-only when they disagree.
3. Contextual lift must survive global and composite stratified shuffle nulls.
