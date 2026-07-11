---
title: "Promotion, Demotion, and Kill Gates"
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

Turns evidence into controlled lifecycle transitions.

# Responsibilities

Require sample, independent cluster count, adjusted statistics, cost survival, cross-feed support, calibration, paper parity, and operational health. Define automatic suspension and human review conditions.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Promoting on one headline metric or keeping a dead strategy because of sunk cost.

# Required tests

Every gate has owner, evidence artifact, timestamp, and rollback.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
