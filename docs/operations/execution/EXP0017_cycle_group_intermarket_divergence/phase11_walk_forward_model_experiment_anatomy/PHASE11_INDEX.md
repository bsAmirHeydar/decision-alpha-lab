# EXP0017 — Phase 11 Index

## Phase name

**Phase 11 — Walk-Forward Validation & Model Experiment Anatomy**

## Purpose

Phase 11 converts the Phase 10 model-ready dataset into a leakage-controlled walk-forward experiment surface. It does not train a complex machine-learning model inside MetaTrader. Instead, it builds disciplined chronological train/test folds, trains a simple bucket-level historical baseline on training windows only, evaluates out-of-sample test windows, and writes audit CSV files.

## Position in the pipeline

```text
Phase 06 Visual/Frontier
  -> Phase 07 Outcome Study
    -> Phase 08 Statistical Reports
      -> Phase 09 Ranking Dashboard
        -> Phase 10 Model Dataset
          -> Phase 11 Walk-Forward Experiment
```

## Core outputs

```text
EXP0017_Phase11_Fold_Plan.csv
EXP0017_Phase11_Predictions.csv
EXP0017_Phase11_Fold_Metrics.csv
EXP0017_Phase11_Bucket_Validation.csv
EXP0017_Phase11_Experiment_Summary.csv
EXP0017_Phase11_Diagnostics.csv
```

## Hard boundary

Phase 11 is still research-only. It does not authorize trading, live filtering, CG removal, risk changes, target changes, model deployment, or AI mutation.
