---
title: "Label and Horizon Factory"
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

Creates multiple outcome views while preserving exact label end times.

# Responsibilities

Classification, regression, ranking, survival, MFE/MAE, path, time-to-resolution, and opportunity-cost labels are versioned.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

One universal win/loss label or purging by entry time instead of label horizon.

# Required tests

Label geometry, same-bar ordering, horizon overlap, and label-version tests.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
