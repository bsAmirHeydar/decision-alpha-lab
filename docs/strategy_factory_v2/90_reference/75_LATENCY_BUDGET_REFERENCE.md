---
title: "Latency Budget Reference"
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

Provides realistic budget design rather than universal promises.

# Responsibilities

Set budgets after benchmarking actual hardware and workload. Python reference paths may target single-digit milliseconds for small local models; compiled MQL5 paths may be lower. Network/broker latency is separate. Monitor distributions and cold starts.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Claiming HFT-class latency without colocation and end-to-end measurement.

# Required tests

Budgets are per strategy generation and mode.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
