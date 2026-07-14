---
title: Model Disagreement and Decision Stability
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Measure whether different credible models, seeds, folds, and assumptions agree on the action rather than only on predictions.

## Capability tier

**Core Production**

## System design

### Disagreement axes

Model family, seed, data bootstrap, cost scenario, fold, feature set, and causal assumption.

### Decision map

Agreement on trade/skip, treatment ID, profile, entry mechanism, and risk tier.

### Instability response

Low decision stability reduces coverage or promotes manual fallback.

### Attribution

Identify whether disagreement comes from eligibility, fill, outcome, rank, or policy threshold.

## Input contracts

- `ChallengerPredictions`
- `ScenarioPredictions`
- `PolicyCompiler`

## Output contracts

- `DisagreementMatrix`
- `StabilityScore`
- `FallbackReason`

## Measurement framework

- Decision agreement.
- Rank correlation.
- Policy flip rate.
- Utility dispersion.

## Adversarial questions

- Do correlated models create false agreement?
- Are disagreements hidden by averaging?
- Does a stable action rely on unstable utility estimates?

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

- [[Multi_Model_Stacking_And_Ensembling]]
