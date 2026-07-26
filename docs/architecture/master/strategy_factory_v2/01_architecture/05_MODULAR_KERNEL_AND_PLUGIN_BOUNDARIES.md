---
title: "Modular Kernel and Plugin Boundaries"
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

Defines the minimal stable kernel and how plugins extend it without creating cross-domain coupling.

# Responsibilities

The kernel owns contracts, plan compilation, context graph execution, candidate identity, decision envelopes, run artifacts, and safety boundaries. Plugins own domain semantics.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Hidden imports, circular dependencies, direct plugin-to-plugin mutation, runtime discovery, and strategy-specific forks of shared services.

# Required tests

Contract tests, capability checks, version compatibility, deterministic replay, and plugin isolation tests.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
