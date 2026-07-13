---
title: "Missing, Stale, and Degraded Context Policy"
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

Turns incomplete data into explicit behavior rather than hidden model input.

# Responsibilities

Classify each feature as required, optional with trained default, or observer-only. Required missing data causes abstention. Staleness limits are feature-specific.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Forward filling across sessions, replacing missing with zero without training equivalence, or trading with desynchronized reference symbols.

# Required tests

Missing, stale, partial feed, DST, reconnect, and feature-version tests.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
