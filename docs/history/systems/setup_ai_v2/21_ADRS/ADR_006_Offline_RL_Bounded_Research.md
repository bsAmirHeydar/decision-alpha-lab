---
title: ADR-006 — Offline RL Is Bounded Research
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- adr
---

# Status

**Accepted**

## Decision

Offline RL is limited to a finite action lattice, no live exploration, conservative evaluation, and deterministic policy compilation.

## Context

SAED V2 combines classical statistical research, frontier machine learning, causal estimation, automated agents, and UCEE runtime integration. Without a hard architectural decision, local optimization could create silent authority or evidence inflation.

## Rationale

Contains support extrapolation and simulator exploitation.

## Consequences

- The rule is machine-enforced where possible.
- Violations block promotion and are recorded as incidents.
- Changes require a superseding ADR, compatibility analysis, and requalification of affected descendants.
