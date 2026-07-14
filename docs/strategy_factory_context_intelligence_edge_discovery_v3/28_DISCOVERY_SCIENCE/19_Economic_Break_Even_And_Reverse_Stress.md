---
title: Economic Break-Even and Reverse Stress
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Find the cost, slippage, latency, capacity, error, and drift levels at which the setup ceases to have positive defensible value.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Outcome distribution.
- Cost/capacity models.
- Uncertainty.

## Output contracts

- Break-even surfaces.
- Operating margin of safety.

## Algorithmic design

- Solve reverse stress for spread, slippage, fill probability, impact, delay, model error, and correlation.
- Use joint rather than one-factor stress.
- Report distance from expected operation to failure boundary.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Stress range not selected to guarantee pass.
- Tail and capacity constraints remain hard.
- Break-even based on lower bound, not mean.

## Measurement system

- Margin to break-even.
- Worst plausible utility.
- Joint stress pass region.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Edge positive only under ideal fill.
- Tiny operational drift erases value.
- Stress assumes independent shocks.

## UCEE integration

- None declared.

## Required tests and evidence

- Joint cost-delay shock.
- Capacity haircut.
- Calibration error.
- Correlation shock.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Multi_Objective_Edge_Utility]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
