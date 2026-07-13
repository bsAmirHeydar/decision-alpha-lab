---
title: "Maximum Anatomy Extraction Program"
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

Extracts every defensible source of value from one anatomy before adding conceptual complexity.

# Responsibilities

Test event existence, direction, timing, location, candidate execution, no-trade filters, failure signals, continuation/reversal duals, holding logic, portfolio overlap, and capacity.

# Fast-path constraints

- All authoritative inputs must be available at the declared decision time.
- Work must be bounded by the compiled plan.
- Runtime failures must map to explicit abstention or rejection reason codes.
- No module may silently change strategy canon, model schema, thresholds, or capital limits.

# Forbidden coupling and failure modes

Adding unrelated concepts to rescue a weak edge.

# Required tests

Matched baselines and component-by-component uplift.

# Operational completion criteria

1. The module has a versioned contract and owner.
2. Inputs, outputs, timestamps, units, and missing behavior are explicit.
3. Deterministic replay is possible from stored artifacts.
4. Performance is benchmarked under the intended mode.
5. Failure behavior is fail-closed when the module is authoritative.
6. Migration and rollback are documented.
