---
title: Learning-to-Rank and Listwise Treatment Choice
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Rank all treatment siblings within an occurrence using listwise objectives aligned with economic regret and abstention.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Occurrence treatment lists.
- Utility distributions and masks.

## Output contracts

- Calibrated ranking.
- Pairwise margins.
- Set-valued shortlist.

## Algorithmic design

- Pairwise, listwise, and differentiable sorting objectives.
- Group by occurrence; never compare unrelated rows as siblings.
- Weight by uncertainty, support, and economic relevance.
- Train against manual, fixed-treatment, and simple score baselines.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No row-random split.
- Ranking metric cannot replace policy value.
- Treatment availability masks enforced.

## Measurement system

- NDCG/regret within occurrence.
- Top-k utility.
- Rank calibration.
- Policy value.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Ranker exploits treatment ID frequency.
- Best treatment unavailable at runtime.
- High ranking accuracy on irrelevant ties.

## UCEE integration

- None declared.

## Required tests and evidence

- Treatment-ID permutation.
- List truncation.
- Near-tie cases.
- Availability mask.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Treatment_Ranking_And_Choice]]
- [[Set_Valued_Treatment_Selection]]
