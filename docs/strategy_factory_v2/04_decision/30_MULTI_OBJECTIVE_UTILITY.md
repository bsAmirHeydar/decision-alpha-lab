---
title: "Multi-Objective Candidate Utility"
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

Ranks candidates using economic utility rather than one label.

# Responsibilities

Possible terms include expected net R, probability positive, target probability, expected MFE, MAE penalty, cost, uncertainty, holding time, capacity, and portfolio overlap. Weights are versioned and validated.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Optimizing raw win rate, mixing incompatible units, or hand-changing weights during live drawdown.

# Required tests

Sensitivity, Pareto, fold stability, and utility decomposition reports.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
