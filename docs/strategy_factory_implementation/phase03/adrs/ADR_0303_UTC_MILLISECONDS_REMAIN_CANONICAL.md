---
title: "ADR 0303 — UTC Milliseconds Remain Canonical"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - adr
---

# Context

Phase 03 required a durable architectural decision.

# Decision

## Decision

Continue Phase 01 UTC epoch-millisecond semantics throughout market services.

## Consequences

Sessions and broker wall times are transformations, never primary identities.

# Status

Accepted.

# Review trigger

Review only when a concrete deployment or compatibility failure demonstrates that the decision no longer serves the platform.
