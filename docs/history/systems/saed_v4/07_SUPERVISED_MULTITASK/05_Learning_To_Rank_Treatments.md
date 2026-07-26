---
title: Learning to Rank Treatments
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Rank sibling treatments within each opportunity cluster while respecting incomplete, censored, and economically constrained outcomes.

## Capability tier

**Core Production**

## System design

### Query group

One context occurrence is one ranking query; all sibling treatments and skip belong to it.

### Objectives

Pairwise, listwise, and utility-aware ranking are compared with simple score baselines.

### Missing comparisons

Non-fill, censoring, ambiguous path, and infeasible candidates are represented explicitly rather than silently removed.

### Selection bridge

Ranking scores are calibrated into utility/support decisions before policy compilation.

## Input contracts

- `OpportunityClusters`
- `CandidateUtilities`
- `FeasibilityMask`

## Output contracts

- `TreatmentRanks`
- `RankUncertainty`
- `SelectionInputs`

## Measurement framework

- NDCG with economic gain.
- Top-k regret.
- Best-treatment selection rate.
- Rank stability.
- Skip rank calibration.

## Adversarial questions

- Are siblings split across folds?
- Does ranking optimize ordinal labels that ignore utility magnitude?
- Is the top-ranked candidate unsupported?

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

- [[Treatment_Effect_Ranking_And_Policy_Value]]
