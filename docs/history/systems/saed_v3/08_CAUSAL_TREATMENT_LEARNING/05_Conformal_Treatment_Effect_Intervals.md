---
title: Conformal Treatment-Effect Intervals
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Attach uncertainty sets to treatment effects and policy gains while respecting the limits of distribution-free individual-effect claims.

## Capability tier

**Governed Challenger**

## System design

### Targets

Intervals for potential outcomes, treatment contrasts, or policy value under clearly stated assumptions.

### Methods

Conformal meta-learners, nested residual conformalization, weighted calibration under shift, and cluster-aware variants.

### Decision use

A treatment is selected only when a conservative lower bound exceeds skip and policy constraints.

### Limit statement

Individual treatment-effect intervals cannot be treated as assumption-free causal guarantees.

## Input contracts

- `CATEPredictions`
- `CalibrationClusters`
- `ShiftWeights`

## Output contracts

- `TreatmentEffectIntervals`
- `CoverageReport`
- `LowerBoundPolicy`

## Measurement framework

- Marginal and subgroup coverage.
- Interval width.
- Coverage under time shift.
- Decision utility from lower bounds.

## Adversarial questions

- Are exchangeability assumptions credible?
- Does adaptive policy selection invalidate coverage?
- Are intervals too wide to support any decision?

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
