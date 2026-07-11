---
title: "ADR 0302 — Terminal APIs Live Behind One Source"
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

All Phase 03 calls to terminal market APIs belong to `CSF03TerminalMarketSource`.

## Consequences

Fixtures and alternative sources can replace terminal access; load and timestamp normalization are centralized.

# Status

Accepted.

# Review trigger

Review only when a concrete deployment or compatibility failure demonstrates that the decision no longer serves the platform.
