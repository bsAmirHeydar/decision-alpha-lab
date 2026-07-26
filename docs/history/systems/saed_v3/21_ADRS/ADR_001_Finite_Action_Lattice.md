---
title: ADR-001 — Finite Action Lattice
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- adr
---

# Status

**Accepted**

## Decision

AI may only select from a versioned compiler-approved finite treatment universe. Open-ended action generation is prohibited.

## Context

SAED V3 combines classical statistical research, frontier machine learning, causal estimation, automated agents, and UCEE runtime integration. Without a hard architectural decision, local optimization could create silent authority or evidence inflation.

## Rationale

Prevents unbounded search, unsupported runtime actions, and non-reproducible policy behavior.

## Consequences

- The rule is machine-enforced where possible.
- Violations block promotion and are recorded as incidents.
- Changes require a superseding ADR, compatibility analysis, and requalification of affected descendants.
