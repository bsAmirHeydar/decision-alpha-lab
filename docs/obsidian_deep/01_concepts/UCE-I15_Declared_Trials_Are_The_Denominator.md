---
title: "UCE-I15 Declared Trials Are The Denominator"
tags: [uce-i15, atomic-concept, strategy-factory]
status: implemented
---
# UCE-I15 Declared Trials Are The Denominator

Multiplicity and reconciliation use every declared trial, including failed, skipped, pruned, and rejected trials.

## Enforcement

- Owned by `strategy_factory_tournament_v3`.
- Covered by executable I15 tests and retained in the release file index.
- Any exception requires a new version, explicit evidence, and downstream compatibility review.

## Consequence

Violating this concept invalidates the affected tournament or prospective-paper evidence rather than merely reducing a score.
