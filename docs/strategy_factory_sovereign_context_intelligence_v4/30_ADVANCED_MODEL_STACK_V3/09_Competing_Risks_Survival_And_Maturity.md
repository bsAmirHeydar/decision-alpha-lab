---
title: Competing-Risks Survival and Maturity
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Model time to fill, stop, target, trail exit, invalidation, expiry, and censoring as competing events.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Event-time outcome traces.
- At-risk intervals.
- Time-varying covariates.

## Output contracts

- Cause-specific hazards.
- Cumulative incidence.
- Expected remaining opportunity life.

## Algorithmic design

- Cause-specific or subdistribution hazards, survival forests/boosting, discrete-time neural survival challengers.
- Time-varying covariates stop at known time.
- Separate fill process from post-fill outcome.
- Use maturity-aware labels and inverse censoring weights only when valid.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No treating censored as loss/win.
- Time origin and risk set explicit.
- Censoring assumptions challenged.

## Measurement system

- Time-dependent Brier.
- Concordance.
- Calibration.
- Decision utility.
- Censoring sensitivity.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Unfilled limit removed.
- Expired Context treated neutral without opportunity cost.
- Future covariates in hazard.

## UCEE integration

- None declared.

## Required tests and evidence

- Administrative censoring.
- Informative censoring sensitivity.
- Competing-event swap.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Survival_And_Competing_Risks]]
- [[Counterfactual_Outcome_Cube_V3]]
