---
title: Runtime Export and Parity
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Export approved preprocessing, models, calibration, thresholds, policy, and treatment state machines into one immutable runtime generation.

## Capability tier

**Core Production**

## System design

### Export paths

Native deterministic representations are primary; ONNX or other formats require capability and operator support.

### Hash binding

Feature order, preprocessing, model, calibration, policy graph, treatment, risk, and monitoring hashes are exact.

### Parity

Python source, exported representation, and MQL5 mirror agree within declared tolerance on golden and adversarial vectors.

### Activation

Partial, stale, incompatible, or unsigned bundles cannot activate.

## Input contracts

- `PromotionAdmission`
- `RuntimeComponents`
- `ConformanceVectors`

## Output contracts

- `ImmutableRuntimeBundle`
- `ParityCertificate`
- `ActivationEvidence`

## Measurement framework

- Prediction parity.
- Decision parity.
- Latency.
- Numerical tolerance.
- Bundle integrity.

## Adversarial questions

- Does export change precision or missing-value behavior?
- Can ONNX fallback silently differ?
- Can runtime load mixed generations?

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

- [[Environment_Reproducibility]]
