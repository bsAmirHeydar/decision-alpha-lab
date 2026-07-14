---
title: Causal Overlap and Positivity Engine
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Determine whether treatment-effect and policy-value claims are identifiable in the observed support.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Treatment assignments or simulated candidate availability.
- Context covariates.
- Sampling and policy history.

## Output contracts

- Overlap map.
- Effective sample size.
- Identifiability state.

## Algorithmic design

- Estimate generalized propensities using cross-fitting.
- Inspect pairwise and multi-action overlap.
- Use overlap weights, trimming policies frozen in advance, and sensitivity surfaces.
- Distinguish designed counterfactual replay from observational human treatment assignment.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No causal claim under structural non-overlap.
- Clipping selected before protected results.
- Report association when ignorability is not defensible.

## Measurement system

- Overlap-weighted ESS.
- Extreme propensity mass.
- Action support coverage.
- Sensitivity to trimming.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Treatment compiler availability mistaken for observed overlap.
- Extreme weights create unstable uplift.
- Human discretion confounding ignored.

## UCEE integration

- None declared.

## Required tests and evidence

- Artificial non-overlap.
- Hidden confounder sensitivity.
- Propensity misspecification.
- Action removal.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Causal_Identification_And_Assumptions]]
- [[Orthogonal_Cross_Fitted_Policy_Value]]
