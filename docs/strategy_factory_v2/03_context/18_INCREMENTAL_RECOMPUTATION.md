---
title: "Incremental Recalculation and State Generations"
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

Avoids rebuilding the entire context when only one input changes.

# Responsibilities

Market adapters increment state generations by symbol/timeframe or coherent state family. Cache keys include event, provider version, and relevant generation. Only affected providers recompute.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Deep-hashing full market state per event, caching without generation, or reusing a value after its source changed.

# Required tests

Generation-change tests, dependency invalidation tests, and stale-cache replay.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
