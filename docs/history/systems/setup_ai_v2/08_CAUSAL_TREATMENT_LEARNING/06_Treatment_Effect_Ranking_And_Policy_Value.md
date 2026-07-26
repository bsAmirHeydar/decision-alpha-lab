---
title: Treatment-Effect Ranking and Policy Value
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Select treatments by incremental value relative to skip or manual baseline rather than by raw predicted outcome alone.

## Capability tier

**Core Production**

## System design

### Reference action

Skip, manual policy, or profile-specific canonical treatment is declared before training.

### Incremental score

Predicted outcome difference, fill-adjusted value, capital-time impact, and uncertainty form the treatment advantage.

### Policy evaluation

Cross-fitted DR estimators and replay estimates are both reported, with disagreement treated as risk.

### Conservative selection

Lower-bound advantage and support conditions are required.

## Input contracts

- `TreatmentEffects`
- `ManualDecisions`
- `Costs`
- `Capacity`

## Output contracts

- `AdvantageScores`
- `PolicyValueReport`
- `SelectionPolicy`

## Measurement framework

- Incremental policy value.
- Regret versus oracle-in-role.
- Selection stability.
- Manual-baseline uplift.

## Adversarial questions

- Does a high raw return simply reflect easier contexts?
- Are policy values estimated on selected folds?
- Is skip value incorrectly fixed at zero when opportunity cost exists?

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

- [[Incremental_Value_Attribution]]
