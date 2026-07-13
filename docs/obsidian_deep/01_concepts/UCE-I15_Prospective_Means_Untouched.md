---
title: "UCE-I15 Prospective Means Untouched"
tags: [uce-i15, atomic-concept, strategy-factory]
status: implemented
---
# UCE-I15 Prospective Means Untouched

A prospective paper period is invalid if any training, tuning, universe mutation, or hidden override uses its observations.

## Enforcement

- Owned by `strategy_factory_tournament_v3`.
- Covered by executable I15 tests and retained in the release file index.
- Any exception requires a new version, explicit evidence, and downstream compatibility review.

## Consequence

Violating this concept invalidates the affected tournament or prospective-paper evidence rather than merely reducing a score.
