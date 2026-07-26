---
title: Conformal Risk Control and Selective Action
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Calibrate prediction sets, action sets, and risk thresholds with explicit assumptions and nonstationarity handling.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Calibration-role scores.
- Loss/risk function.
- Selection policy.

## Output contracts

- Coverage/risk-controlled set or abstention directive.

## Algorithmic design

- Split/cross conformal where exchangeability is plausible.
- Risk-control or learn-then-test style thresholding for monotone losses.
- Selective conformal sets for actions.
- Rolling/weighted/online variants as challengers under drift.
- Report assumption scope.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No universal guarantee claim under shift.
- Calibration data isolated.
- Coverage monitored by subgroup and time.

## Measurement system

- Empirical coverage.
- Risk bound.
- Set size.
- Selective utility.
- Coverage decay.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Conformal interval interpreted probability.
- Threshold reused after regime change.
- Small calibration set overclaimed.

## UCEE integration

- None declared.

## Required tests and evidence

- Exchangeable simulation.
- Abrupt shift.
- Gradual drift.
- Subgroup coverage.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Conformal_Uncertainty_Abstention_Control]]
- [[Frontier_Research_Register_2026]]
