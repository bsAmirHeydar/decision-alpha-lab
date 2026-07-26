---
title: "Plugin SDK Overview"
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

Defines the extension surface for anatomy, features, candidates, models, decisions, risk, and execution.

# Responsibilities

Every plugin has a descriptor, narrow interface, deterministic identity, explicit dependencies, version, capabilities, tests, and failure behavior.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Plugins performing file I/O in live calls, inspecting outcome labels, allocating capital outside risk, or changing canon.

# Required tests

Unit, contract, metamorphic, latency, and differential tests before registration.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
