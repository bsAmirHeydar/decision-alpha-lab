---
title: "Fixed-Order Feature Vectors"
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

Removes dataframe and dictionary ambiguity from model inference.

# Responsibilities

Each model route uses a versioned schema with exact names, order, defaults, scaling artifact, and strictness. Candidate-specific numeric values are appended through declared fields.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Alphabetical feature order, implicit categorical encoding, or changing defaults without model retraining.

# Required tests

Golden vector hashes, missing-feature behavior, single/batch parity, and cross-language vector parity.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
