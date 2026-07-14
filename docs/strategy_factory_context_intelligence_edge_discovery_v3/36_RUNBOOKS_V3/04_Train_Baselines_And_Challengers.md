---
title: Train Baselines and Challengers
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v3
  - runbook
  - operations
---

# Mission

Execute the model ladder from manual and simple baselines to advanced challengers on identical folds, costs, and candidate sets.

## Entry conditions

- Frozen dataset/folds.
- Task graph.
- Model and compute budget.

## Mandatory roles and separation of duties

- Model engineer.
- Statistical adversary.
- Model-risk reviewer.

## Procedure

1. Train Skip-all, fixed-treatment, manual, naive, regularized, calibrated tree, survival, distributional, ranking, and advanced candidates.
2. Cross-fit preprocessing and nuisances.
3. Record every trial, retry, prune, timeout, and exposure.
4. Calibrate on allowed role.
5. Create model/system cards.
6. Run ablations and simple-equivalent tests.

## Mandatory outputs

- Complete trial universe.
- Model artifacts.
- Baseline ladder report.
- Calibration and support reports.

## Stop and escalation conditions

- Fold leakage.
- Trial ledger incomplete.
- Advanced model lacks protected incremental value.
- Runtime infeasible without justified distillation.

## Evidence retained

- Manifests.
- Logs.
- Predictions.
- Failure artifacts.
- Cards.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Advanced_Model_Stack_Charter]]
- [[Complete_Trial_And_Exposure_Universe]]
