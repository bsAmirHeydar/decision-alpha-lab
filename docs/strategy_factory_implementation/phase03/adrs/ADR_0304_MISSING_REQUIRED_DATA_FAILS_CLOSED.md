---
title: "ADR 0304 — Missing Required Data Fails Closed"
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

Gapped, stale, missing, or desynchronized required data cannot produce a live-capable decision.

## Consequences

The platform may abstain more often, but avoids silent fabricated context.

# Status

Accepted.

# Review trigger

Review only when a concrete deployment or compatibility failure demonstrates that the decision no longer serves the platform.
