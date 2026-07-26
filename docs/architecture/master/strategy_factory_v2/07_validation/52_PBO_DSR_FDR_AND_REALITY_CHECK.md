---
title: "PBO, Deflated Sharpe, FDR, and Reality Check"
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

Quantifies the chance that the selected winner is a product of search.

# Responsibilities

PBO evaluates rank reversal across combinations; DSR deflates performance for trials/non-normality; BH controls false discoveries; reality check tests the best rule against a null distribution.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Using these as decorative metrics without counting the full search universe.

# Required tests

Predeclare families and report both raw and adjusted results.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
