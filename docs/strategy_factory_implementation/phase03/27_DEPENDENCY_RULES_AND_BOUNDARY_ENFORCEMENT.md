---
title: "Dependency Rules and Boundary Enforcement"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Rules

```text
Contracts → Contracts
Core → Contracts + Core
Ports → Contracts + Core + Ports
Market → Contracts + Core + Ports + Market
Testing → all non-live Phase 03 layers
```

## Forbidden

- Market importing Anatomy, Candidate, Risk, or Execution.
- Contracts importing Market.
- Terminal API calls outside terminal source.
- Order authority anywhere in Phase 03.
- Strategy terminology inside market services.

## Enforcement

Machine-readable rules live in:

```text
lab/11_strategy_factory/phase03_market/config/dependency_rules_v3.json
```

Static tests and `check_sf03_boundaries.py` inspect source files.

## Design rationale

Compile-time boundaries are more reliable than documentation alone. A future contributor should receive a failing test immediately when placing logic in the wrong layer.

## Extension rule

A new market source implements `ISF03MarketSource`. It must not alter cache or synchronization contracts. A new time provider implements the clock port or extends the kernel behind a versioned mode.
