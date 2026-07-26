# Phase 12 Research Data Contract

## Required files

The workbench expects at least:

- `EXP0017_Phase10_Model_Dataset.csv`
- `EXP0017_Phase11_Predictions.csv`
- `EXP0017_Phase11_Fold_Metrics.csv`
- `EXP0017_Phase11_Bucket_Validation.csv`

Missing files are not silently ignored. They appear in the data audit output.

## Primary grouping

The workbench attempts to use `bucket_key` if it exists. If no bucket key exists, it reconstructs a fallback key from:

- `group`
- `direction`
- `role_key`

## Primary outcome

The workbench reads actual R from one of these fields if present:

- `actual_r`
- `primary_r`
- `actual_primary_r`

This keeps Phase 12 tolerant to minor naming differences in prior CSVs.
