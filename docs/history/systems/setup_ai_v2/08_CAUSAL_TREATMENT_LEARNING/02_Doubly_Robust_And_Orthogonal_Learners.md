---
title: Doubly Robust and Orthogonal Learners
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- governed-challenger
---

# Purpose

Estimate conditional treatment effects and policy value with nuisance-robust, cross-fitted procedures.

## Capability tier

**Governed Challenger**

## System design

### Nuisance models

Outcome regressions and treatment propensities are trained out-of-fold.

### Orthogonal scores

AIPW, R-learner, DR-learner, and orthogonal random forest variants reduce first-order nuisance sensitivity.

### Cross-fitting

All pseudo-outcomes are produced without in-row model fitting.

### Diagnostics

Extreme propensities, effective sample size, residual bias, and nuisance instability are reported.

## Input contracts

- `AssignmentModel`
- `OutcomeModel`
- `CrossFitFolds`

## Output contracts

- `PseudoOutcomes`
- `CATEEstimates`
- `DRPolicyValue`

## Measurement framework

- Policy value with robust standard errors.
- CATE calibration.
- Overlap-weighted effective sample size.
- Nuisance sensitivity.

## Adversarial questions

- Are propensities artificial because treatments came from a simulator?
- Are extreme weights clipped after seeing results?
- Does cross-fitting preserve time order and clusters?

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

- [[Causal_Forests_And_Heterogeneity]]
