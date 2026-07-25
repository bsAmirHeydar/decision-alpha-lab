# Strategy Factory Phase 03 — Shared Market Services

This additive patch implements the strategy-blind MQL5-first market, time,
session, synchronization, and symbol-specification core.

## Main entry points

- `mql5/Include/AlphaLab/StrategyFactory/Market/SF03_AllMarket.mqh`
- `mql5/Experts/StrategyFactoryTests/SF03_MarketServicesSelfTest.mq5`
- `mql5/Experts/StrategyFactory/SF03_MarketServicesDiagnostic.mq5`
- `lab/11_strategy_factory/python/strategy_factory_market/`
- `docs/strategy_factory_implementation/phase03/00_PHASE_03_MOC.md`

## Important scope boundary

No legacy anatomy, candidate, risk, or execution code is integrated in this
phase. The central engine is completed first.

## Authority

MQL5 owns market, time, synchronization, and broker-symbol truth. Python is an
offline conformance and research mirror.

## Acceptance

Automated Python/static tests pass in the build environment. MetaEditor
compilation and terminal execution must be completed locally before the phase
is marked fully accepted.
