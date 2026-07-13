---
title: "Immutable Generations and Atomic Hot Swap"
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

Supports rapid updates without partial state or mixed model/config versions.

# Responsibilities

A generation contains plan, provider graph, candidate factory, model artifacts, thresholds, hashes, and reason-code vocabulary. Requests pin one generation from start to finish.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Mutating an active object in place, loading half a model, or mixing old vectors with new coefficients.

# Required tests

Shadow load, warmup, self-test, atomic pointer swap, rollback, and generation-level telemetry.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
