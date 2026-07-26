# Phase 11 — Validation and Test Plan

## Compile checks

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_WalkForward_Model_Experiment_Anatomy.mq5
```

## Data checks

1. Run Phase 07.
2. Run Phase 08.
3. Run Phase 09.
4. Run Phase 10.
5. Confirm `EXP0017_Phase10_Model_Dataset.csv` exists.
6. Run Phase 11.

## Expected files

```text
EXP0017_Phase11_Fold_Plan.csv
EXP0017_Phase11_Predictions.csv
EXP0017_Phase11_Fold_Metrics.csv
EXP0017_Phase11_Bucket_Validation.csv
EXP0017_Phase11_Experiment_Summary.csv
EXP0017_Phase11_Diagnostics.csv
```

## Key validations

- Test samples must be after train samples.
- Embargo window must sit between train and test.
- Folds with insufficient sample count must be marked unusable.
- Predictions must only be produced for test windows.
- Bucket statistics must only use train-window rows.
- No chart orders or trading calls should exist.

## Diagnostic failure cases

```text
missing_phase10_dataset
invalid_phase10_header
no_rows_for_walk_forward
failed_no_usable_folds
```
