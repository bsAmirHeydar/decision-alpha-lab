---
title: "Sequence and Representation Models"
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

Adds pre-event path information only after event/tabular baselines are stable.

# Responsibilities

Use causal windows ending at decision time, normalized returns/volatility, masks, and train-only preprocessing. Compare against summary features.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Chart screenshots, future-normalized windows, overlapping train/test sequences, or huge models on few independent events.

# Required tests

Purged sequence folds, representation ablation, and event-cluster sample accounting.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
