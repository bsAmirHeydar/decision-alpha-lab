# Phase 11 — Data Contract

## Input

```text
EXP0017_Phase10_Model_Dataset.csv
```

Required columns include:

```text
sample_id
signal_id
model_use_status
group
direction
role_key
confirmation_broker
confirmation_ny
primary_r
mfe_r
mae_r
label_binary_win
label_stopped_intraday
```

## Fold plan output

```text
EXP0017_Phase11_Fold_Plan.csv
```

Columns:

```text
fold_id
train_start
train_end
embargo_start
embargo_end
test_start
test_end
train_count
test_count
usable
status
```

## Prediction output

```text
EXP0017_Phase11_Predictions.csv
```

Each row is an out-of-sample test sample.

Important columns:

```text
fold_id
sample_id
bucket_key
bucket_source
train_count_for_bucket
predicted_avg_r
predicted_win_rate
predicted_edge_class
actual_r
actual_win
actual_stop
directional_agreement
```

## Bucket validation output

```text
EXP0017_Phase11_Bucket_Validation.csv
```

This records what each training bucket looked like in each fold.

## Fold metrics output

```text
EXP0017_Phase11_Fold_Metrics.csv
```

This summarizes out-of-sample performance overall, by fold, by bucket, and by fold-bucket.
