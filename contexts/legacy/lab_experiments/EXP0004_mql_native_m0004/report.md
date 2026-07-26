# EXP0004 — MQL-native M0004 Branch Regime Clustering

This experiment runs `M0004_BranchRegimeClustering.mq5` on a target symbol/timeframe and reads final Journal lines beginning with `DAL_M0004_FINAL_`.

Required sanity line:

```text
DAL_M0004_BUILD_SANITY ... build=1.00 ... branchSequence=chronological_M0002_exit_labels
```

Primary output lines:

```text
DAL_M0004_FINAL_TRANSITION
DAL_M0004_FINAL_RUNS
DAL_M0004_FINAL_TRANSITION_PERM_STRESS
DAL_M0004_FINAL_RUN_SHUFFLE_STRESS
DAL_M0004_FINAL_BLOCK_CONCENTRATION_STRESS
```

Acceptance is documented in `docs/operations/mql5_native/H0004_BRANCH_REGIME_CLUSTERING.md`.
