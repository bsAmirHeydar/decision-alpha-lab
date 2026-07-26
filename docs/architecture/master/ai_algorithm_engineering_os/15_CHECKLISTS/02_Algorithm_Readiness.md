---
id: AIEOS-E476AE0592
title: "Algorithm Readiness Checklist"
type: checklist
status: active
domain: checklist
version: 1.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - checklist
  - checklist
---
# Algorithm Readiness Checklist

> [!abstract] Purpose
> Decide whether an algorithm is ready for implementation

## Definition

- [ ] Inputs, outputs, units, timing, and missing-data behavior are explicit.
- [ ] State and event identities are stable.

## Correctness

- [ ] Transitions and invariants cover all legal and illegal paths.
- [ ] No future information is required.
- [ ] Pseudocode is deterministic and implementation-independent.

## Operations

- [ ] Complexity budgets, reconstruction, restart, and idempotency are defined.
- [ ] Failure and diagnostic behavior are specified.

## Evidence

- [ ] Examples, counterexamples, edge cases, and test matrix exist.
- [ ] A reviewer can simulate the algorithm from the artifacts.

## Gate Result

- **PASS:** every mandatory item is checked and evidence is linked.
- **CONDITIONAL:** only explicitly accepted, time-bounded exceptions remain.
- **FAIL:** any domain rule, safety rule, compilation rule, or state-integrity item is unresolved.

## Evidence Record

| Item | Evidence link / command output | Reviewer | Date |
|---|---|---|---|
|  |  |  |  |

## Related Notes

- [[17_GOVERNANCE/02_Quality_Gates|Quality Gates]]
- [[17_GOVERNANCE/06_Definition_of_Done|Definition of Done]]
