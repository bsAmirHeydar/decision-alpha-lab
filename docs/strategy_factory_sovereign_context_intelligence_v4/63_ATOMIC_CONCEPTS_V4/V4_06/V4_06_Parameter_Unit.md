---
title: Parameter Unit
status: implemented
version: 1.0.0
phase: V4-06
created: '2026-07-15'
updated: '2026-07-15'
capability_tier: core-production-context-plane
tags: [saed-v4, v4-06, treatment-dsl]
---

# Parameter Unit

## Definition

The explicit semantic measurement domain attached to every parameter.

## Why it exists

Units prevent silent comparison of points, milliseconds, fractions and R multiples.

## Invariants

- The concept is bound to exact registry, policy, capability, graph, handoff, Evidence Role and known-time identities.
- Its canonical form is deterministic and contains no executable callback, dynamic code or network dependency.
- Unknown, conflicting, stale, over-budget or authority-violating inputs fail closed.
- It cannot train a model, select a Treatment, size a position, allocate capital, activate runtime or submit an order.

## Validation

The reference implementation exercises the concept through golden artifacts and targeted negative fixtures. Integrity and replay evidence must reproduce the same content identities. Any semantic mutation requires a new hash and explicit downstream review.

## Related

- [[00_MOC_V4_06_Treatment_DSL]]
- [[26_Static_Type_Checking]]
- [[55_Acceptance_Criteria]]
- [[57_Limitations_And_Residual_Risk]]
