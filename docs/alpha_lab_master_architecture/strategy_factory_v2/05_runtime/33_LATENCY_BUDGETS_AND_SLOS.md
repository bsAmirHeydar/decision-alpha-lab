---
title: "Latency Budgets and Service-Level Objectives"
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

Turns speed into measurable stage-level requirements.

# Responsibilities

Measure context, gates, candidate build, model inference, ranking, risk, broker preflight, total, and queue delay. Track p50/p95/p99 and breach reason.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Advertising a fixed latency without hardware and topology evidence, optimizing averages only, or hiding cold-start behavior.

# Required tests

Warm/cold benchmarks, burst tests, percentile gates, and production telemetry.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
