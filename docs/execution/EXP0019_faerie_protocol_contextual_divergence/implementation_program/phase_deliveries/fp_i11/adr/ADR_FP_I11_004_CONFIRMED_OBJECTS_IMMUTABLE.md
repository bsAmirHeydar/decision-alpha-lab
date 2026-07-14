---
title: "Confirmed Objects Are Immutable"
tags: [exp0019, faerie-protocol, fp-i11, indicator, visual-projection, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I11
phase_version: 1.0.0
last_updated: 2026-07-13
language: en
---

# Confirmed Objects Are Immutable

## Decision

Historical confirmed and terminal evidence cannot be silently mutated.

## Consequences

- Deterministic replay and restart.
- No Indicator/EA semantic divergence.
- Explicit failure instead of silent repaint.
- Versioned migration when the contract changes.

## Status

Accepted for FP-I11 version 1.0.0.
