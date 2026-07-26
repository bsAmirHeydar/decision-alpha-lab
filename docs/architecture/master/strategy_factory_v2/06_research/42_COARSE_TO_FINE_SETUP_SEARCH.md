---
title: "Coarse-to-Fine Setup Search"
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

Searches broad execution possibilities without exhausting the statistical budget.

# Responsibilities

Stage 1 coarse entry/stop/exit families; stage 2 retain train-stable regions; stage 3 refine parameters; stage 4 freeze finalists; stage 5 untouched confirmation.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Fine grid search over all data or selecting isolated parameter peaks.

# Required tests

Parameter-surface smoothness, neighborhood stability, trial count, and confirmation holdout.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
