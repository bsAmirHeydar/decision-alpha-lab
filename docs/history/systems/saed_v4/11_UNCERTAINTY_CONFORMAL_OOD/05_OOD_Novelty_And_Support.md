---
title: OOD, Novelty and Support
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Detect when an opportunity, treatment, or representation lies outside reliable training support.

## Capability tier

**Core Production**

## System design

### Support layers

Context support, feature support, representation distance, treatment assignment support, view completeness, and regime support.

### Detectors

Density/ratio methods, kNN/Mahalanobis, one-class models, ensemble disagreement, conformal scores, and classifier-based shift tests.

### Composite policy

No detector is authoritative alone; a rule combines hard support violations and calibrated soft novelty.

### Response

Simpler model, manual fallback, skip, quarantine, or research capture.

## Input contracts

- `FeatureSnapshot`
- `Representation`
- `TrainingSupportIndex`

## Output contracts

- `SupportAudit`
- `NoveltyScore`
- `FallbackDirective`

## Measurement framework

- OOD detection on held-out domains.
- False alarm rate.
- Risk conditional on novelty.
- Fallback utility.

## Adversarial questions

- Does the detector learn symbol identity?
- Can a novel but benign state cause permanent abstention?
- Does support drift unnoticed because embedding changes?

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

- [[Conformal_Prediction_For_Time_Series]]
