---
title: "Zero-I/O and Allocation Discipline"
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

Protects the authoritative thread from unpredictable pauses.

# Responsibilities

No file/network/database calls; preallocate bounded arrays where practical; reuse context frames; avoid dataframe construction; serialize on observer paths.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Synchronous log writes, loading models on demand, dynamic JSON, or unbounded strings in the hot path.

# Required tests

Static audits, allocation profiling, log-failure injection, and long-run memory tests.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
