---
title: ADR-002 — Capability Tier Separation
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

All methods are classified as Core Production, Governed Challenger, Research-Only, or Prohibited-to-Live.

## Context

SAED V4 combines classical statistical research, frontier machine learning, causal estimation, automated agents, and UCEE runtime integration. Without a hard architectural decision, local optimization could create silent authority or evidence inflation.

## Rationale

Allows frontier research without granting frontier models premature authority.

## Consequences

- The rule is machine-enforced where possible.
- Violations block promotion and are recorded as incidents.
- Changes require a superseding ADR, compatibility analysis, and requalification of affected descendants.
