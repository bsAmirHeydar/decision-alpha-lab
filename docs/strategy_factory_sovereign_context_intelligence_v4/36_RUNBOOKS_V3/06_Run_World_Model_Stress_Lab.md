---
title: Run the World-Model Stress Lab
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v4
  - runbook
  - operations
---

# Mission

Search for rare-path and regime failures using synthetic trajectories without using synthetic success as promotion evidence.

## Entry conditions

- Qualified stress model.
- Frozen candidate policy.
- Intervention library.

## Mandatory roles and separation of duties

- World-model researcher.
- Statistical adversary.
- Execution auditor.
- Model-risk reviewer.

## Procedure

1. Validate model on held-out real paths.
2. Freeze interventions.
3. Generate volatility, gap, liquidity, correlation, path-order, and regime stresses.
4. Search for policy exploitation and failures.
5. Compare ensemble disagreement.
6. Classify findings.

## Mandatory outputs

- Synthetic stress corpus.
- Failure findings.
- Simulator-limitations card.

## Stop and escalation conditions

- Synthetic data mixed with real evidence.
- Policy exploits simulator.
- Critical failure without containment.

## Evidence retained

- Generator/model hashes.
- Intervention seeds.
- Synthetic labels.
- Failure trace.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[World_Model_Stress_And_Rare_Regime_Lab]]
- [[Synthetic_Evidence_Classification]]
