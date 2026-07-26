# EXP0017 — Phase 10 Model-Ready Dataset Anatomy

Phase 10 converts Phase 07 signal-level outcome rows and optional Phase 09 ranking evidence into a single row-level dataset that can be used for offline research, model prototyping, notebook analysis, and later supervised decision-support experiments.

Phase 10 is not an execution layer. It does not decide trades, block trades, rank live signals, mutate cycle groups, change risk, or optimize the strategy.

## Inputs

- `EXP0017_Phase07_Outcome_Study.csv`
- optional `EXP0017_Phase09_Rankings_All.csv`
- optional `EXP0017_Phase09_Shortlist.csv`

## Outputs

- `EXP0017_Phase10_Model_Dataset.csv`
- `EXP0017_Phase10_Feature_Dictionary.csv`
- `EXP0017_Phase10_Label_Summary.csv`
- `EXP0017_Phase10_Diagnostics.csv`

## Core principle

A confirmed divergence sample becomes a feature row only after its outcome is measurable. The row preserves raw anatomy, time context, role context, risk context, outcome labels, and optional statistical enrichment.
