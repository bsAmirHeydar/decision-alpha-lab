---
title: "Precompiled Candidate Templates"
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

Replaces runtime Cartesian search with a promoted bounded set.

# Responsibilities

Research selects compatible entry/stop/exit templates. Startup resolves callables and parameters. Runtime builds at most the declared budget.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Generating all combinations live, changing reward targets from model output without a declared policy, or truncating candidates by arbitrary insertion order.

# Required tests

Template identity, priority, compatibility, geometry, and count-budget tests.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
