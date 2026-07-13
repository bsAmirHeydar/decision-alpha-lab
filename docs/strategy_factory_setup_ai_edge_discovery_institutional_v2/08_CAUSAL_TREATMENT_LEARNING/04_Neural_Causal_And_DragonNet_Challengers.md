---
title: Neural Causal and DragonNet Challengers
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- governed-challenger
---

# Purpose

Evaluate representation-based neural treatment-effect models only when they improve robust policy value over orthogonal baselines.

## Capability tier

**Governed Challenger**

## System design

### Architectures

TARNet/DragonNet-style shared representation with treatment-specific outcome heads and propensity regularization.

### Multi-treatment extension

Finite treatment lattice uses structured embeddings and masked heads; unsupported treatments remain masked.

### Cross-fitting

Neural nuisance and treatment models are generated out-of-fold with seed ensembles.

### Governance

Neural causal claims require overlap, sensitivity, and simpler-model agreement.

## Input contracts

- `TreatmentRows`
- `ContextRepresentation`
- `PropensityTargets`

## Output contracts

- `NeuralCATE`
- `PolicyScores`
- `CausalModelCard`

## Measurement framework

- DR policy value.
- CATE calibration.
- Seed variance.
- Representation balance.
- Incremental utility.

## Adversarial questions

- Does the representation erase effect modifiers?
- Does targeted regularization overfit the selected policy?
- Are multi-treatment propensities too sparse?

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

- [[Doubly_Robust_And_Orthogonal_Learners]]
