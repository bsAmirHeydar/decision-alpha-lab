---
title: "Context and Decision Cache Hierarchy"
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

Reduces repeated computation without weakening causality.

# Responsibilities

L0 local provider values, L1 event context cache, L2 shared session/reference cache, and optional offline feature store. Each record has version and TTL.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Caching outcomes, cross-contaminating symbols, using wall-clock TTL without source generation, and unbounded memory.

# Required tests

Eviction, expiry, version mismatch, concurrency, and deterministic cache-hit tests.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
