---
title: ADR-018 — Compute Budget Protects Falsification and Replication
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v3
  - adr
  - adr-018
---

# Status

Accepted for SAED V3 architecture.

## Context

The institutional Context-learning platform must scale model and research sophistication without weakening known-time truth, evidence, authority, risk, runtime, or operational controls.

## Decision

Red-team and reproduction budgets cannot be consumed by model search.

## Rationale

Prevents compute scale from weakening science.

## Consequences

### Positive

- The decision creates an explicit, testable institutional boundary.
- Artifacts and downstream systems can rely on stable semantics.
- Failure and fallback behavior can be predeclared.

### Trade-offs

- Fewer frontier experiments can run.
- Exceptions require a new ADR, compatibility review, tests, and evidence reset where material.

## Enforcement

- Closed contracts and schemas.
- Boundary and mutation tests.
- Independent validation.
- UCEE admission and runtime handoff checks.

## Related notes

- [[Ultimate_Institutional_Design_Standard]]
- [[Three_Lines_Model_Risk_Governance]]
