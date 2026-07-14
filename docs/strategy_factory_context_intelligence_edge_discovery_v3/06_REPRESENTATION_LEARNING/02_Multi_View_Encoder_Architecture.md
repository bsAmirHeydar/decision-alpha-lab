---
title: Multi-View Encoder Architecture
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Fuse structural, temporal, intermarket, execution, and context views without losing missingness, known time, or view-specific uncertainty.

## Capability tier

**Core Production**

## System design

### View encoders

Each semantic view has a typed encoder and missing-view token rather than naïve imputation.

### Fusion modes

Late fusion is the Core baseline; gated attention, cross-attention, and graph fusion are governed challengers.

### View dropout

Training includes controlled view dropout to measure dependency and ensure safe degradation.

### Attribution

Per-view uplift, conditional value, disagreement, and failure under removal are recorded.

## Input contracts

- `ViewSnapshotBundle`
- `MissingnessMask`
- `EncoderVersions`

## Output contracts

- `FusedRepresentation`
- `ViewAttribution`
- `RequiredViewPolicy`

## Measurement framework

- Performance under view removal.
- Cross-view disagreement calibration.
- Incremental value by view.
- Latency and exportability.

## Adversarial questions

- Does one high-capacity view dominate through leakage?
- Can missingness itself reveal outcomes?
- Does runtime have all views with the same timing?

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

- [[OOD_Novelty_And_Support]]
