---
title: "Context Fingerprint and Lineage"
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

Makes every decision reproducible from exact source versions and values.

# Responsibilities

Hash event identity, snapshot schema, feature values, feature versions, state generations, and provider plan. Store the fingerprint in the DecisionEnvelope.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Hashing only the final vector, omitting missing reasons, or losing the link to raw feed and anatomy version.

# Required tests

Rebuild verification and artifact lineage audits.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
