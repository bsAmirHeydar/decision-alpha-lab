---
title: Calibration and Decision Thresholds
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Separate score learning, probability calibration, utility mapping, and operational threshold selection.

## Capability tier

**Core Production**

## System design

### Calibration roles

Calibration data is distinct from model fitting and final selection.

### Methods

Platt, isotonic, beta, temperature, vector, and distribution calibration are selected per task.

### Threshold policy

Thresholds optimize bounded utility under coverage, risk, capacity, and profile constraints inside nested validation.

### Drift response

Calibration failure reduces coverage or triggers fallback; runtime does not silently recalibrate.

## Input contracts

- `RawScores`
- `CalibrationFold`
- `ObjectiveProfile`

## Output contracts

- `CalibratedOutputs`
- `ThresholdPolicy`
- `CalibrationCard`

## Measurement framework

- ECE and classwise calibration.
- Brier/proper score.
- Coverage-risk curve.
- Threshold stability.

## Adversarial questions

- Is isotonic overfitting small samples?
- Were thresholds selected on the same fold reported?
- Does calibration hold in tails and rare contexts?

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
