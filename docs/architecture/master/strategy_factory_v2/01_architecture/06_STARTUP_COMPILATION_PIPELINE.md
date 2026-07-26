---
title: "Startup Compilation Pipeline"
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

Moves expensive configuration, discovery, validation, graph sorting, and template expansion out of the market-event path.

# Responsibilities

Load spec; validate schema; resolve exact plugin versions; compile feature DAG; compile vector schemas; pre-resolve policy callables; prune templates; load model artifacts; validate hashes; warm caches; publish immutable generation.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Parsing JSON per tick, dynamic imports per event, runtime Cartesian products, unresolved model versions, and partial startup.

# Required tests

Compilation must be deterministic, hash-addressed, fail-closed, and fully inspectable.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
