# Phase 11 — Walk-Forward Experiment Specification

## Problem

Up to Phase 10, the system can produce a row-level dataset. That dataset is useful, but if it is evaluated incorrectly it can create false confidence. The main risk is leakage: using information from the future to judge or score signals in the past.

Phase 11 fixes the evaluation discipline.

## Walk-forward doctrine

A valid research experiment must use this structure:

```text
Training window: historical samples only
Embargo window: gap between train and test to reduce adjacency leakage
Test window: future samples not seen during training
```

The experiment then rolls forward:

```text
Fold 1: train A -> test B
Fold 2: train B-ish -> test C
Fold 3: train C-ish -> test D
...
```

## Baseline model

Phase 11 intentionally uses a simple baseline rather than a complex model:

```text
bucket key -> average primary_r and win_rate in training window
```

Default bucket key:

```text
CG | direction | hunter-clean role
```

Example:

```text
cg_30m | BUY | SPXUSD_hunter__NDXUSD_clean
```

## Why simple baseline first?

A complex model should not be introduced until the system knows whether simple stable buckets have out-of-sample structure. If the baseline cannot survive walk-forward testing, a complex model may only memorize noise.

## Evaluation

Each test sample receives a training-derived baseline:

```text
predicted_avg_r
predicted_win_rate
predicted_edge_class
```

Then Phase 11 compares this against actual test outcome:

```text
actual_r
actual_win
actual_stop
actual_mfe_r
actual_mae_r
```

## Research interpretation

A good bucket is not simply one that looked good in all history. A useful bucket is one whose training-window quality survives in the unseen test window across folds.
