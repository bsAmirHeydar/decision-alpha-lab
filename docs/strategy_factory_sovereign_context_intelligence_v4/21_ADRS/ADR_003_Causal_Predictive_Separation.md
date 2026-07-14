---
title: ADR-003 — Causal and Predictive Separation
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- adr
---

# Status

**Accepted**

## Decision

Predictive ranking, simulator counterfactuals, and causal treatment-effect claims use separate contracts and evidence standards.

## Context

SAED V4 combines classical statistical research, frontier machine learning, causal estimation, automated agents, and UCEE runtime integration. Without a hard architectural decision, local optimization could create silent authority or evidence inflation.

## Rationale

Prevents predictive success from being misrepresented as causal identification.

## Consequences

- The rule is machine-enforced where possible.
- Violations block promotion and are recorded as incidents.
- Changes require a superseding ADR, compatibility analysis, and requalification of affected descendants.
