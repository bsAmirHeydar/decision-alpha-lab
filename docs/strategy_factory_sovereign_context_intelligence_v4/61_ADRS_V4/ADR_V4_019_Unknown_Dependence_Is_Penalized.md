---
title: ADR V4-019 — Unknown Dependence Is Penalized
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
  - adr
  - governance
---

# Decision

Unknown Dependence Is Penalized.

## Context

SAED V4 operates a large adaptive research program with advanced models, agents and distributed infrastructure. Without an explicit decision, implementation convenience could silently weaken scientific validity or authority boundaries.

## Consequences

- Contracts and tests must encode this decision.
- Violations fail closed and create an incident.
- Exceptions require a signed waiver with owner, rationale, evidence, expiry and rollback.
- The waiver cannot grant order, risk, promotion or runtime authority to AI.

## Alternatives rejected

- Informal convention.
- Trusting model confidence.
- Allowing hidden state or undocumented manual override.
- Deferring the issue to production monitoring.

## Verification

Negative and mutation tests must demonstrate that violating the decision is detected before protected evaluation or runtime activation.
