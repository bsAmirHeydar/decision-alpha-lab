# Phase 13 Validation and Test Plan

## Static checks

- Python syntax compile;
- PowerShell path review;
- MQL5 include dependency review;
- ZIP integrity review.

## Automated smoke test

The included standard-library test generates:

- a synthetic Phase 10 dataset;
- three walk-forward folds;
- a Phase 12.5 READY status;
- deterministic classification and regression comparisons.

The test asserts:

- successful execution;
- leaderboard creation;
- at least two usable folds;
- execution authority remains false.

## Real-data validation

- run Phase 12.5 first;
- compare row/fold counts against Phase 11;
- confirm fixed fold identities;
- review leakage audit;
- inspect calibration bins;
- inspect coefficient stability;
- verify repeated runs with the same seed are identical;
- compare with bucket baseline before interpreting any advanced model.
