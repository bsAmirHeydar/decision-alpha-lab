---
title: "New Anatomy Fast Onboarding"
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

Defines the shortest defensible route from an existing anatomy engine to a paper decision.

# Responsibilities

Freeze doctrine; scaffold plugin; map event fields; add shared and specific providers; select 3 to 12 candidate templates; define matched null; add golden fixtures; run dataset and baseline; compile plan; shadow; paper.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Building a new statistics, trainer, dashboard, or executor.

# Required tests

The first thin vertical slice should prioritize one event, one context snapshot, a small candidate set, one baseline, one model route, and paper trace.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
