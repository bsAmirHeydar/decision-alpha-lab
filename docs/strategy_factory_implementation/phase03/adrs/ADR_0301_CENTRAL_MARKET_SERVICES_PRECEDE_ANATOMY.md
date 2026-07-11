---
title: "ADR 0301 — Central Market Services Precede Anatomy"
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

Complete and validate market/time/symbol services before connecting existing anatomies.

## Consequences

Core defects are isolated from strategy defects. Migration is delayed slightly, but every later adapter becomes smaller and more consistent.

# Status

Accepted.

# Review trigger

Review only when a concrete deployment or compatibility failure demonstrates that the decision no longer serves the platform.
