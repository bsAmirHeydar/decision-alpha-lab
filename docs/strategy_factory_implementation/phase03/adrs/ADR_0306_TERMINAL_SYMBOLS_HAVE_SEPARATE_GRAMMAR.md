---
title: "ADR 0306 — Terminal Symbols Have Separate Grammar"
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

Broker symbols use a dedicated safety validator rather than internal identifier grammar.

## Consequences

Real broker naming is supported without weakening internal IDs or wire delimiters.

# Status

Accepted.

# Review trigger

Review only when a concrete deployment or compatibility failure demonstrates that the decision no longer serves the platform.
