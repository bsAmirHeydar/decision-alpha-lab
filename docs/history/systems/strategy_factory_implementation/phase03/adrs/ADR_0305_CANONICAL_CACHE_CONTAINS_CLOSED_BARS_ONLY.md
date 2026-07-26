---
title: "ADR 0305 — Canonical Cache Contains Closed Bars Only"
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

The shared bar cache imports closed bars only. Forming-bar/tick state is separate.

## Consequences

New-bar and known-time semantics become stable across tester, paper, and live.

# Status

Accepted.

# Review trigger

Review only when a concrete deployment or compatibility failure demonstrates that the decision no longer serves the platform.
