---
title: "Purged Nested Walk-Forward"
domain: strategy-factory-v2
status: canonical
language: en
version: 2.0.0
tags:
  - alpha-lab
  - strategy-factory
  - anatomy-to-decision
---

# Purpose

Separates hyperparameter and threshold selection from final fold evaluation.

# Responsibilities

Outer folds estimate performance. Inner purged folds choose features, candidates, models, calibration, and thresholds. Purge uses label end; embargo follows market dependence.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Choosing thresholds on outer test or using fixed one-day embargo regardless of holding horizon.

# Required tests

Fold timeline audit and cluster disjointness.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
