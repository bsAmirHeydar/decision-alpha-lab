---
title: Distributional Outcome and Tail Models
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Estimate the full treatment outcome distribution, including asymmetry, multimodality, heavy tails, and conditional expected shortfall.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Outcome cube.
- Context/treatment representation.
- Censoring masks.

## Output contracts

- Quantiles, mixture distribution, tail metrics, calibration.

## Algorithmic design

- Quantile regression, distributional boosting, mixture density networks, normalizing-flow challengers, and calibrated empirical residual distributions.
- Use profile-specific tails and separate zero/non-fill mass.
- Evaluate distribution calibration and tail coverage.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No Gaussian assumption by default.
- Tail metrics require sufficient effective samples and conservative pooling.
- Complex distributions compete with empirical baselines.

## Measurement system

- CRPS.
- Pinball loss.
- Tail coverage.
- Expected shortfall error.
- Decision utility.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Mean prediction hides ruinous tail.
- Flow extrapolates unsupported extremes.
- Tail calibrated on final data.

## UCEE integration

- None declared.

## Required tests and evidence

- Heavy-tail synthetic benchmark.
- Best-trade removal.
- Tail event holdout.
- Quantile crossing.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Distributional_Survival_And_Tail_Learning]]
- [[Payoff_Profile_Specific_Estimands]]
