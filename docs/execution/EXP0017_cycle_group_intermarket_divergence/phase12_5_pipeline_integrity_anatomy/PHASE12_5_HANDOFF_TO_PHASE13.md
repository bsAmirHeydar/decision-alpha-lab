# Phase 12.5 Handoff to Phase 13

Phase 13 is permitted only after the readiness output is reviewed.

## Required evidence package

- file audit;
- schema issues;
- duplicate report;
- lineage reconciliation;
- semantic issues;
- temporal audit;
- metric reconciliation;
- readiness gates;
- readiness summary.

## Phase 13 objective

Controlled model comparison should compare simple, reproducible candidates against the Phase 11 bucket baseline:

1. bucket baseline;
2. threshold baseline;
3. logistic classifier;
4. ridge/linear R regression;
5. constrained ensemble.

## Phase 13 constraints

- fixed walk-forward folds;
- deterministic seeds;
- no future-derived features;
- calibration and error analysis;
- model cards;
- no execution authority;
- no automatic strategy mutation.

If Phase 12.5 reports `BLOCKED_FOR_PHASE13`, Phase 13 work must stop until the integrity defect is resolved.
