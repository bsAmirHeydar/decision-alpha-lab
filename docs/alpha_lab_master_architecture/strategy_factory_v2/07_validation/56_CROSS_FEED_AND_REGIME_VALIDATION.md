---
title: "Cross-Feed, Cross-Instrument, and Regime Validation"
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

Distinguishes economic structure from one feed or period artifact.

# Responsibilities

Canonical futures/venue data, target broker data, alternate broker, adjacent instruments, different volatility/macro regimes, and session-calendar changes.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Pooling feeds without source IDs or assuming a CFD divergence equals futures price discovery.

# Required tests

Report direction and magnitude consistency, not just pooled significance.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
