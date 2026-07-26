---
title: "Central Engine First Policy"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Decision

The Strategy Factory will be completed centrally before legacy strategy engines are migrated. Existing strategy code remains in its current system until shared contracts, market services, plugin boundaries, candidate infrastructure, and test harnesses are stable.

## Why

Migrating legacy strategies too early creates two forms of coupling:

1. The new core begins to inherit historical assumptions from one strategy.
2. Strategy defects become indistinguishable from platform defects.

A central-first sequence allows the core to be validated with fixtures. When a real strategy is later connected, any discrepancy can be classified as an adapter or doctrine issue rather than an undefined infrastructure issue.

## Enforcement

Phase 03 source code is prohibited from containing strategy vocabulary such as:

- Hook
- F1/F2/F3
- Zone
- Divergence
- Hunter/Clean
- Daye
- ICT
- Astro

The central engine may expose generic concepts only:

- symbol
- timeframe
- tick
- closed bar
- known time
- session
- data quality
- synchronization requirement
- specification generation

## Migration consequence

Legacy modules will later be evaluated under four choices:

```text
reuse through adapter
wrap behind a port
migrate into a shared capability
retire after parity validation
```

No legacy module is copied into the central engine merely because it already works. Reuse requires contract compatibility, causal-time compliance, bounded runtime behavior, and fixture parity.

## Success condition

A fixture anatomy plugin in Phase 04 must be able to run using only the Phase 01–03 platform. The first real strategy integration should then require adapter work, not modifications to market/time/symbol services.
