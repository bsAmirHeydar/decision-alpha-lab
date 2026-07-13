---
title: "Multi-Strategy Portfolio Layer"
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

Combines promoted strategies by true risk and event dependence.

# Responsibilities

Cluster underlying theses, estimate PnL and tail dependence, cap shared event risk, allocate by robustness/capacity, and preserve strategy-level attribution.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Treating differently named strategies as diversified when they trade the same NY expansion.

# Required tests

Cluster-level stress, correlation regimes, common-loss episodes, and marginal contribution.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
