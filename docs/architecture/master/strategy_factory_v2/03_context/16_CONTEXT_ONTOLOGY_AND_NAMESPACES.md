---
title: "Context Ontology and Namespaces"
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

Keeps thousands of possible features organized, versioned, and collision-free.

# Responsibilities

Use namespaces such as market.*, time.*, anatomy.*, intermarket.*, execution.*, account.*, and candidate.*. Each feature has unit, type, source, known time, update trigger, and semantic version.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Ambiguous names like strength, range, or quality without unit and source; reusing a name after changing meaning.

# Required tests

Schema registry checks and semantic compatibility tests.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
