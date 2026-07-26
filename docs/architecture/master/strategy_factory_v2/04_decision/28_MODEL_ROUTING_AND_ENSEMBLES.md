---
title: "Model Routing and Ensembles"
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

Routes exact vectors to approved model artifacts and combines outputs transparently.

# Responsibilities

Each route names model/version, vector schema, output mapping, required status, calibration, and fallback. Ensembles are explicit weighted or stacked artifacts trained without test leakage.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Model auto-discovery, implicit output names, remote fallback, or averaging incompatible probabilities.

# Required tests

Artifact hash, route completeness, calibration, challenger shadow, and inference parity tests.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
