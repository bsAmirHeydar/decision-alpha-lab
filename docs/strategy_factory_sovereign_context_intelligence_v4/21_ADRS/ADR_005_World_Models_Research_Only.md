---
title: ADR-005 — World Models Are Research-Only
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

World models and generated paths support representation and stress research but cannot replace historical, paper, or live evidence.

## Context

SAED V4 combines classical statistical research, frontier machine learning, causal estimation, automated agents, and UCEE runtime integration. Without a hard architectural decision, local optimization could create silent authority or evidence inflation.

## Rationale

Prevents model-generated worlds from manufacturing statistical confidence.

## Consequences

- The rule is machine-enforced where possible.
- Violations block promotion and are recorded as incidents.
- Changes require a superseding ADR, compatibility analysis, and requalification of affected descendants.
