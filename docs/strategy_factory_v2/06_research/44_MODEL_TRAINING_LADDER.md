---
title: "Model Training Ladder"
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

Escalates model complexity only when simpler baselines are insufficient.

# Responsibilities

Never/always trade, threshold, logistic/ridge, boosted trees, calibrated rankers, sequence encoders, contextual bandits. Each stage must demonstrate incremental OOS value.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Jumping directly to deep learning or RL, or optimizing model metrics unrelated to economic utility.

# Required tests

Baseline delta, calibration, ablation, latency, stability, and complexity penalty.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
