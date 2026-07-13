---
title: ADR-004 — Agents Cannot Promote
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

AI agents can propose, build, challenge, and summarize but cannot sign promotion or production authorization.

## Context

SAED V2 combines classical statistical research, frontier machine learning, causal estimation, automated agents, and UCEE runtime integration. Without a hard architectural decision, local optimization could create silent authority or evidence inflation.

## Rationale

Maintains separation of duties and human accountability.

## Consequences

- The rule is machine-enforced where possible.
- Violations block promotion and are recorded as incidents.
- Changes require a superseding ADR, compatibility analysis, and requalification of affected descendants.
