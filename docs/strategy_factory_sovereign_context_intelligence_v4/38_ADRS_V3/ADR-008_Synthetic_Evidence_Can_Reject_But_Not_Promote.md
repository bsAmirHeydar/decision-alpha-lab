---
title: ADR-008 — Synthetic Evidence Can Reject But Not Promote
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v4
  - adr
  - adr-008
---

# Status

Accepted for SAED V4 architecture.

## Context

The institutional Context-learning platform must scale model and research sophistication without weakening known-time truth, evidence, authority, risk, runtime, or operational controls.

## Decision

World-model and synthetic stress success has zero promotion weight; critical failure can block.

## Rationale

Prevents simulator alpha while retaining falsification value.

## Consequences

### Positive

- The decision creates an explicit, testable institutional boundary.
- Artifacts and downstream systems can rely on stable semantics.
- Failure and fallback behavior can be predeclared.

### Trade-offs

- Synthetic research cannot accelerate promotion directly.
- Exceptions require a new ADR, compatibility review, tests, and evidence reset where material.

## Enforcement

- Closed contracts and schemas.
- Boundary and mutation tests.
- Independent validation.
- UCEE admission and runtime handoff checks.

## Related notes

- [[Ultimate_Institutional_Design_Standard]]
- [[Three_Lines_Model_Risk_Governance]]
