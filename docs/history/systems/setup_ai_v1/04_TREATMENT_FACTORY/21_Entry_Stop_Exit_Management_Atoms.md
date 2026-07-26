---
id: SAED-8AB19F7538
title: "Entry, Stop, Exit, and Management Atom Registries"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - treatment
  - atoms
---

# Entry, Stop, Exit, and Management Atom Registries

## Entry Atoms

Market, breakout stop, limit at structural level, reclaim, close confirmation, retest, staggered entry and cancel/expiry rules.

## Stop Atoms

Wide structural invalidation, tight trigger invalidation, Context invalidation, volatility-buffered stop, confirmation-candle extreme, reference/zone boundary and maximum-loss cap.

## Exit Atoms

Fixed R, structural destination, liquidity destination, opposite Context, partial+runner, open trail, time exit and emergency exit.

## Management Atoms

Break-even, trailing activation, ratchet update, partials, re-entry, scale-in prohibition/permission, expiry, position-time health and Context invalidation.

## Registry Requirements

Each atom declares version, parameters, direction semantics, known-time inputs, state machine, side-aware price usage, broker constraints, path-dependence, runtime support and tests.
