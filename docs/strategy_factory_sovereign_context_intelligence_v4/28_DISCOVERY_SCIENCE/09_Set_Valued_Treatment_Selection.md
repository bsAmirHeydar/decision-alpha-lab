---
title: Set-Valued Treatment Selection
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Return a safe set of statistically indistinguishable treatments or abstain when point selection is not defensible.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Treatment score distributions.
- Pairwise uncertainty.
- Operational constraints.

## Output contracts

- Candidate set.
- Dominance and ambiguity reasons.

## Algorithmic design

- Construct confidence sets around treatment utility.
- Remove candidates dominated under conservative bounds.
- Pass set to deterministic manual/rule tie-breaker or portfolio layer.
- Shrink set only with calibration-role evidence.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No arbitrary argmax under overlapping uncertainty.
- Tie-breaker cannot use protected outcomes.
- Set size and coverage monitored.

## Measurement system

- Set coverage.
- Average set size.
- Regret of selected member.
- Abstention rate.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Numerically highest score treated certain.
- Tie-break changes across runtime implementations.
- Set excludes true best due to leakage.

## UCEE integration

- None declared.

## Required tests and evidence

- Near-tie synthetic cases.
- Calibration drift.
- Python/MQL5 deterministic tie-break.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Selectivity_Coverage_And_Abstention_Frontier]]
- [[Treatment_Ranking_And_Choice]]
