---
title: "V1 to V2 Migration"
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

Migrates the existing Strategy Factory without discarding its research artifacts.

# Responsibilities

Keep V1 contracts and batch pipeline. Add V2 plugin descriptors, context DAG, compiled plan, fixed vectors, fast decision engine, generation management, latency telemetry, and MQL5 runtime contracts. Adapt one strategy end to end before mass migration.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Big-bang rewrite or changing anatomy and infrastructure simultaneously.

# Required tests

Differential replay must show V1/V2 research equivalence where semantics are unchanged.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
