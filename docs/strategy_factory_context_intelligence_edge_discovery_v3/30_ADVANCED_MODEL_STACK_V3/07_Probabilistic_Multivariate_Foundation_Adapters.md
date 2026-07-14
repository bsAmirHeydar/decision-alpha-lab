---
title: Probabilistic Multivariate Foundation Adapters
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Adapt univariate or generic foundation models to multivariate, probabilistic, treatment-conditioned Context tasks without full uncontrolled retraining.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Foundation encoder.
- Cross-variable adapter.
- Target-domain calibration roles.

## Output contracts

- Probabilistic multivariate forecasts/embeddings.
- Adapter dossier.

## Algorithmic design

- Frozen backbone plus cross-series adapter, low-rank adaptation, or mixture-of-experts routing.
- Produce distributions or quantiles, not point-only forecasts.
- Condition on Context and treatment descriptors.
- Calibrate per horizon and support bucket.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Adapter selection nested.
- No target-final fine-tuning.
- Compare specialized classical models.

## Measurement system

- CRPS/pinball plus treatment utility.
- Calibration.
- Sample efficiency.
- Transfer stability.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Forecast metric improves but selection utility falls.
- Cross-series adapter leaks future contemporaneous variables.
- Fine-tuning overfits small Context.

## UCEE integration

- None declared.

## Required tests and evidence

- Leave-variable-out.
- Few-shot curves.
- Adapter rank sweep.
- Cross-domain transport.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Foundation_Model_Intake_V3]]
- [[Distributional_Outcome_And_Tail_Models]]
