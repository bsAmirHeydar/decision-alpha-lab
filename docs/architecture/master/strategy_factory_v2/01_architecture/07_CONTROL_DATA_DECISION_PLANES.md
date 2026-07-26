---
title: "Control, Data, and Decision Planes"
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

Separates configuration and governance from market data and authoritative decisions.

# Responsibilities

Control plane promotes versions and deploys plans. Data plane ingests and timestamps market state. Decision plane performs bounded in-memory computation. Observer plane records non-authoritative telemetry.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Letting dashboards, loggers, retrainers, or remote services block or mutate the decision path.

# Required tests

Fault injection proving observer failure cannot change authoritative output.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
