---
title: "Model Plugin"
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

Provides a stable predict-one and predict-batch interface for promoted artifacts.

# Responsibilities

Declare exact feature order, artifact hash, output names, deterministic mode, local/remote capability, calibration contract, and missing behavior.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Training in the decision process, implicit feature order, internet dependency, nondeterministic inference, or unversioned preprocessing.

# Required tests

Golden vectors, batch/single parity, schema mismatch, latency, and numerical stability tests.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
