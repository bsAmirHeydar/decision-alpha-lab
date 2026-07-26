---
title: Time-Series Foundation Model Adapters
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Use pretrained time-series foundation models as bounded feature generators or challengers, never as unverified trading oracles.

## Capability tier

**Governed Challenger**

## System design

### Adapter boundary

Frozen zero-shot forecasts, embeddings, likelihoods, or fine-tuned adapters are materialized as versioned features.

### Model intake

License, provenance, architecture, training-domain disclosure, supply-chain integrity, and reproducibility are reviewed.

### Benchmark discipline

TimesFM-, Chronos-, MOMENT-, Moirai-, and MoE-style capabilities are compared with native baselines on economic tasks, not forecasting benchmarks alone.

### Financial caution

Strong generic forecasting rank does not imply useful trading edge; economic incremental value and stability are mandatory.

## Input contracts

- `FoundationModelIntake`
- `AdapterConfig`
- `PretrainingDisclosure`

## Output contracts

- `AdapterFeatures`
- `FoundationModelCard`
- `SupplyChainAttestation`

## Measurement framework

- Economic uplift after costs.
- Calibration and tail coverage.
- Domain-shift robustness.
- Compute and latency cost.
- Dependency risk.

## Adversarial questions

- Does a public checkpoint contain overlapping market periods?
- Is zero-shot success a benchmark artifact?
- Can opaque pretraining invalidate data-role claims?

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

- [[Capability_Tier_Policy]]
