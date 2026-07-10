# EXP0017 Phase 12 — Research Workbench Notebook Template

This markdown notebook template defines the inspection order for Python or Jupyter review.

## 1. Load files

- Phase 10 model dataset
- Phase 11 walk-forward predictions
- Phase 11 fold metrics
- Phase 11 bucket validation

## 2. Data audit

Check row counts, missing columns, model-ready rows, and fold coverage.

## 3. Out-of-sample leaderboard

Sort by:

1. minimum sample count
2. average out-of-sample R
3. win rate
4. stop rate
5. fold coverage

## 4. Bucket stability

A bucket is not good because it has one strong fold. A bucket becomes interesting only if its behavior is repeated across folds.

## 5. Drift and fragility

Check if feature distributions in prediction/test rows differ materially from the full dataset.

## 6. Decision boundary

The notebook may produce research candidates, not trading permission.
