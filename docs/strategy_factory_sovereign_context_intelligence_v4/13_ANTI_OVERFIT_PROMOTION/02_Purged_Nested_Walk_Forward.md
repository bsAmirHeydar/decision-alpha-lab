---
title: Purged Nested Walk-Forward
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Separate model fitting, tuning, calibration, selection, and reporting along chronological and dependency-aware boundaries.

## Capability tier

**Core Production**

## System design

### Outer folds

Estimate selection procedure performance through time.

### Inner folds

Choose features, model family, hyperparameters, thresholds, and calibration.

### Purge

Remove observations whose information or label windows overlap validation.

### Embargo

Prevent near-boundary dependence and slow information diffusion.

### Cluster assignment

Opportunity and shared-event clusters remain intact.

## Input contracts

- `DatasetManifest`
- `DependencyGraph`
- `LabelWindows`

## Output contracts

- `FoldManifest`
- `PurgeLedger`
- `OuterPredictions`

## Measurement framework

- Fold coverage.
- Purged fraction.
- Temporal gap.
- Outer-fold dispersion.
- Selection stability.

## Adversarial questions

- Does preprocessing fit across outer folds?
- Are trail labels overlapping through long holds?
- Are context siblings split?

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

- [[Nested_Selection_And_Model_Family_Risk]]
