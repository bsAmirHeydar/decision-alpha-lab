---
title: "Terminal Market Source Boundary"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Sole terminal adapter

`CSF03TerminalMarketSource` is the only Phase 03 module authorized to call:

- `SymbolSelect`;
- `SymbolInfoTick`;
- `CopyRates`;
- `SymbolInfoDouble`;
- `SymbolInfoInteger`.

Static tests enforce this boundary.

## Benefits

- terminal behavior is mockable;
- fixture tests require no broker;
- time conversion occurs once;
- all bars receive the same source lineage;
- future vendor adapters can implement the same source interface;
- strategy code cannot create accidental load through repeated `CopyRates`.

## Bar import behavior

- current forming bar is skipped;
- returned rates are normalized oldest-to-newest;
- server timestamps are converted to UTC;
- Phase 01 bar contracts are created;
- no strategy-specific filtering occurs.

## Known limitation

Timeframe conversion currently supports standard MetaTrader timeframes. Non-standard synthetic intervals will be implemented above the source through a resampling capability rather than by changing terminal calls.
