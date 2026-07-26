---
title: "Decision Envelope and Explanation"
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

Captures everything required to audit why a decision occurred.

# Responsibilities

Store event, candidate set, scores, selected candidate, action, reason codes, context/plan/model hashes, timestamps, latency, calibration, thresholds, and bounded explanations.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Free-text-only explanations, post-hoc recomputation, or explanations that use data outside the decision path.

# Required tests

Round-trip serialization, lineage reconstruction, and exact replay.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
