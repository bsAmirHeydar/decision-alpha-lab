---
title: "Recommended Deployment Sequence"
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

Minimizes risk while delivering speed.

# Responsibilities

Phase 1 compile/inspect only; Phase 2 replay; Phase 3 shadow decisions; Phase 4 paper; Phase 5 micro-live; Phase 6 limited live; Phase 7 scale. Start with EXP0017, then NDS Zone-AF, then additional anatomies.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Enabling live because the runtime is technically capable.

# Required tests

Every phase has rollback and evidence gates.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
