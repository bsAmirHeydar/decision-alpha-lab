---
title: "Context-to-Decision Fast Path"
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

Defines the authoritative low-latency path from a confirmed event to a bounded decision.

# Responsibilities

No I/O; no parsing; no dynamic discovery; bounded features, providers, candidates, models, and gates; local inference; explicit abstention; stage timing.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Running research searches, remote inference, report generation, logging serialization, or unbounded loops in the decision thread.

# Required tests

Warm/cold benchmark, p50/p95/p99, deterministic replay, failure fallback, and budget-breach behavior.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
