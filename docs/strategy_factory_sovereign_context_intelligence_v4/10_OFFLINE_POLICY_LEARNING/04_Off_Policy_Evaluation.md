---
title: Off-Policy Evaluation
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- research-only
---

# Purpose

Estimate policy value without deployment using multiple estimators and explicit diagnostics for support and model error.

## Capability tier

**Research-Only**

## System design

### Estimators

Direct method, importance sampling variants, doubly robust, marginalized estimators, fitted Q evaluation, and replay-based structural evaluation.

### Cross-fitting

Nuisance and value models are trained out-of-fold and cluster-aware.

### Triangulation

No single estimator can authorize promotion; disagreement increases model risk.

### Stress

Costs, action propensities, missing actions, and hidden confounding are perturbed.

## Input contracts

- `EvaluationPolicy`
- `BehaviorPolicy`
- `OfflineDataset`

## Output contracts

- `OPEBundle`
- `EstimatorDisagreement`
- `PolicyValueBounds`

## Measurement framework

- Estimator agreement.
- Effective sample size.
- Weight concentration.
- Confidence interval width.
- Stress stability.

## Adversarial questions

- Are propensities near zero?
- Does one estimator dominate because of its own model assumptions?
- Is replay treated as unbiased observed policy data?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[Causal_Identification_And_Assumptions]]
