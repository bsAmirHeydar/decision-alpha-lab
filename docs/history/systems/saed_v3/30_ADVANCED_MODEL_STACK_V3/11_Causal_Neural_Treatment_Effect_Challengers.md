---
title: Causal Neural Treatment-Effect Challengers
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Use flexible neural treatment-effect models only after identification, overlap, and orthogonal baselines are established.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Cross-fitted causal dataset.
- Treatment and support masks.

## Output contracts

- CATE distributions.
- Policy-value challenger.

## Algorithmic design

- Shared representation with treatment-specific heads, balancing penalties, targeted regularization, or latent-confounder sensitivity challengers.
- Cross-fit all representations where feasible.
- Compare against DR/R/forest baselines.
- Conformalize or bootstrap effects.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Neural CATE cannot fix non-identification.
- No causal wording without assumptions.
- Architecture search counted fully.

## Measurement system

- CATE calibration.
- Policy value.
- Overlap-bucket stability.
- Negative-control response.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Balanced representation hides non-overlap.
- Neural model overfits pseudo-outcomes.
- Effect interpreted mechanistically.

## UCEE integration

- None declared.

## Required tests and evidence

- Placebo treatment.
- Hidden-confounder sensitivity.
- Architecture ablation.
- Cross-fit leakage.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Neural_Causal_And_DragonNet_Challengers]]
- [[Orthogonal_Cross_Fitted_Policy_Value]]
