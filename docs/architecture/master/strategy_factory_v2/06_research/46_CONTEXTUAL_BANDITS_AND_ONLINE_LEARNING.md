---
title: "Contextual Bandits and Controlled Online Learning"
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

Adapts policy selection without granting uncontrolled self-modification.

# Responsibilities

Begin in shadow/paper. Use bounded action set, delayed rewards, propensity logging, conservative updates, offline policy evaluation, and rollback.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Full RL against live capital, unlogged exploration, or changing anatomy definitions online.

# Required tests

Counterfactual evaluation, safety constraints, drift, and regret monitoring.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
