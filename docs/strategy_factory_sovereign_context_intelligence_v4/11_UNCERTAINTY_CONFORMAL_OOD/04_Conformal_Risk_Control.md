---
title: Conformal Risk Control
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Calibrate decision thresholds to control an operational loss or risk functional rather than merely prediction-set coverage.

## Capability tier

**Core Production**

## System design

### Risk functions

False-trade rate, expected shortfall breach, unsupported selection, excessive drawdown contribution, or profile-specific loss.

### Calibration

Thresholds are selected on dedicated chronological calibration roles.

### Selection interaction

Adaptive treatment selection is included in the calibration pipeline.

### Runtime policy

If assumptions or calibration freshness fail, thresholds tighten or decisions abstain.

## Input contracts

- `CalibrationLosses`
- `CandidateScores`
- `RiskTarget`

## Output contracts

- `RiskControlledThreshold`
- `RiskCertificate`
- `ExpiryPolicy`

## Measurement framework

- Controlled empirical risk.
- Coverage.
- Risk under shift.
- Threshold stability.

## Adversarial questions

- Is the loss bounded as required?
- Does selection after calibration invalidate control?
- Are guarantees described beyond their assumptions?

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

- [[Abstention_Is_Alpha_Protection]]
