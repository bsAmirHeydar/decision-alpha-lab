---
title: "Phase 03 — Shared Market Services MOC"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Phase 03 — Shared Market Services

> Establish one canonical MQL5-owned source for market data, time, session identity, multi-symbol synchronization, and broker symbol specifications before any anatomy plugin is integrated.

## Status

**Implemented in code; local MetaEditor compilation and terminal diagnostics remain mandatory acceptance evidence.**

## Architectural position

Phase 03 is deliberately strategy-blind. It does not know what a Hook, F3, Zone, SMT divergence, Daye cycle, ICT sequence, or structural node means. Those concepts will arrive later through adapters. This phase owns only the facts every strategy must consume consistently:

```text
terminal ticks and closed bars
→ canonical UTC timestamps
→ bounded caches
→ gap and staleness state
→ session/trading-day identity
→ multi-symbol synchronization
→ versioned symbol specifications
→ typed health and telemetry
```

## Navigation

### Authority and architecture

- [[01_PHASE_CHARTER_AND_EXIT_GATE]]
- [[02_CENTRAL_ENGINE_FIRST_POLICY]]
- [[03_MARKET_TIME_AND_SYMBOL_TRUTH_AUTHORITY]]
- [[04_REFERENCE_ARCHITECTURE_AND_DATA_FLOW]]
- [[27_DEPENDENCY_RULES_AND_BOUNDARY_ENFORCEMENT]]

### Time

- [[05_TIME_KERNEL_REFERENCE]]
- [[06_BROKER_TIME_TO_UTC_MAPPING]]
- [[07_NEW_YORK_DST_AND_GOLDEN_FIXTURES]]
- [[08_TRADING_DAY_AND_SESSION_PRIMITIVES]]

### Market state

- [[09_TICK_CACHE_REFERENCE]]
- [[10_CLOSED_BAR_CACHE_REFERENCE]]
- [[11_CANONICAL_NEW_BAR_IDENTITY]]
- [[12_MULTI_SYMBOL_SYNCHRONIZATION]]
- [[13_MISSING_BAR_AND_GAP_POLICY]]
- [[14_STALE_DATA_AND_FRESHNESS_POLICY]]

### Broker metadata

- [[15_SYMBOL_SPECIFICATION_CACHE]]
- [[16_SPECIFICATION_GENERATION_AND_DRIFT]]
- [[17_TERMINAL_MARKET_SOURCE_BOUNDARY]]

### Operations and quality

- [[18_SERVICE_LIFECYCLE_AND_COMPOSITION]]
- [[19_MARKET_HEALTH_AND_TELEMETRY]]
- [[20_PERFORMANCE_MEMORY_AND_CACHE_BUDGETS]]
- [[21_FAILURE_SEMANTICS_AND_FAIL_CLOSED_RULES]]
- [[31_DATA_QUALITY_STATE_MACHINE]]
- [[32_MARKET_STATE_GENERATIONS_AND_DIRTY_PROPAGATION]]
- [[33_GAP_RECOVERY_AND_SERIES_REBUILD_PROTOCOL]]
- [[34_FIXTURE_CATALOG_AND_GOLDEN_CASE_POLICY]]
- [[35_MARKET_SOURCE_EXTENSION_GUIDE]]
- [[36_REENTRANCY_CALLBACK_AND_STATE_OWNERSHIP]]
- [[37_RUN_MANIFEST_MARKET_FIELDS]]
- [[38_MARKET_SERVICES_SECURITY_AND_AUTHORITY]]
- [[39_PHASE03_PERFORMANCE_ACCEPTANCE_PLAN]]
- [[40_PHASE03_DECISION_LOG_AND_ROADMAP_IMPACT]]
- [[24_TEST_MATRIX_AND_ACCEPTANCE_EVIDENCE]]
- [[25_LOCAL_COMPILE_AND_DIAGNOSTIC_RUNBOOK]]
- [[29_DEFINITION_OF_DONE]]
- [[30_KNOWN_LIMITATIONS_AND_DEFERRED_WORK]]

### Language mirrors and handoff

- [[22_MQL5_API_REFERENCE]]
- [[23_PYTHON_CONFORMANCE_MIRROR]]
- [[26_PHASE01_BROKER_SYMBOL_COMPATIBILITY_HOTFIX]]
- [[28_PHASE04_HANDOFF_STATIC_PLUGIN_REGISTRY]]

## Code entry points

```text
mql5/Include/AlphaLab/StrategyFactory/Market/SF03_AllMarket.mqh
mql5/Experts/StrategyFactoryTests/SF03_MarketServicesSelfTest.mq5
mql5/Experts/StrategyFactory/SF03_MarketServicesDiagnostic.mq5
lab/11_strategy_factory/python/strategy_factory_market/
```

## Non-negotiable rule

No strategy module may call `CopyRates`, `SymbolInfoTick`, `SymbolInfoDouble`, `SymbolInfoInteger`, or perform timezone conversion directly after this phase. All such access must flow through the shared services or an explicitly versioned source adapter.
