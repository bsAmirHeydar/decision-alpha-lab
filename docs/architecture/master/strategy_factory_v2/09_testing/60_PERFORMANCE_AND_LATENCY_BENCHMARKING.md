---
title: "Performance and Latency Benchmarking"
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

Produces reproducible latency and throughput evidence.

# Responsibilities

Specify hardware, OS, Python/MQL5 version, warmup, event/candidate/features/models, cache state, p50/p95/p99/max, throughput, allocations, and failure rate.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Comparing different workloads or quoting best single call.

# Required tests

Store benchmark manifests and regressions in CI thresholds.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
