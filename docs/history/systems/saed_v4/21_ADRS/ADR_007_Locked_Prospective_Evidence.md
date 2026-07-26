---
title: ADR-007 — Locked Prospective Evidence
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

Every promoted candidate requires a frozen prospective challenge unless an explicitly signed governance exception defines a narrower non-live use.

## Context

SAED V4 combines classical statistical research, frontier machine learning, causal estimation, automated agents, and UCEE runtime integration. Without a hard architectural decision, local optimization could create silent authority or evidence inflation.

## Rationale

Makes selection and operational deltas visible.

## Consequences

- The rule is machine-enforced where possible.
- Violations block promotion and are recorded as incidents.
- Changes require a superseding ADR, compatibility analysis, and requalification of affected descendants.
