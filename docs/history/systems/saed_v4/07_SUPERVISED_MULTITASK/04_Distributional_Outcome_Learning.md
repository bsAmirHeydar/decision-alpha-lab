---
title: Distributional Outcome Learning
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Estimate the full conditional distribution of net returns, MFE, MAE, holding time, and path outcomes instead of a fragile point forecast.

## Capability tier

**Core Production**

## System design

### Distribution targets

Quantiles, expectiles, mixture distributions, discrete bins, or parametric families selected inside nested folds.

### Joint structure

Return, MFE, MAE, fill, and time may be linked through multi-output models with coherent constraints.

### Tail focus

Expected shortfall, probability of large win, probability of full stop, and downside quantiles are first-class.

### Calibration

Probability integral transform, quantile coverage, tail calibration, and conditional coverage are reported.

## Input contracts

- `TreatmentRows`
- `NetOutcomeTargets`
- `ClusterWeights`

## Output contracts

- `OutcomeDistribution`
- `TailMetrics`
- `DistributionCalibration`

## Measurement framework

- CRPS or proper scoring rule.
- Quantile coverage.
- Tail calibration.
- Economic utility from predicted distribution.

## Adversarial questions

- Does the model predict impossible MFE/MAE relations?
- Are tails learned from too few independent clusters?
- Is a point estimate used where path asymmetry matters?

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

- [[Distributionally_Robust_Utility]]
