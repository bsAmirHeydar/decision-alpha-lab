---
title: Conformal Prediction for Time Series
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Construct empirical prediction sets while explicitly addressing non-exchangeability, dependence, and regime shift.

## Capability tier

**Core Production**

## System design

### Calibration units

Opportunity clusters rather than treatment rows.

### Methods

Rolling, weighted, adaptive, block, and online conformal variants are compared with ordinary split conformal.

### Coverage scope

Marginal, horizon, profile, regime, and selected-policy coverage are reported separately.

### Limitations

Coverage can fail under rapid shift or adaptive reuse; the system responds with reduced coverage or abstention.

## Input contracts

- `CalibrationPredictions`
- `ClusterOrder`
- `ShiftWeights`

## Output contracts

- `PredictionSets`
- `CoverageReport`
- `ConformalState`

## Measurement framework

- Empirical coverage.
- Conditional coverage gaps.
- Set width.
- Coverage under shift.

## Adversarial questions

- Are calibration scores dependent across overlapping windows?
- Is adaptive tuning using the same failures it reports?
- Does narrow width come from undercoverage?

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

- [[Conformal_Risk_Control]]
