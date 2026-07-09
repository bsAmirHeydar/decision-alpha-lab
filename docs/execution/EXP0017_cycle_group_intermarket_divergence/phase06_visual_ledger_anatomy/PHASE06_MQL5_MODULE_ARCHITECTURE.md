# Phase 06 MQL5 Module Architecture

## Expert

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

The expert configures inputs, enables symbols, initializes all CG toggles, and delegates processing to `CCGV_Engine`.

## Includes

```text
CGV_Types.mqh       # config and visual-ledger state types
CGV_Drawing.mqh     # chart-object creation and cleanup
CGV_Ledger.mqh      # CSV append-only audit ledger
CGV_Display.mqh     # chart panel and print summary
CGV_Engine.mqh      # orchestration over Phase 01–05 anatomy
```

## Dependency rule

Phase 06 must not duplicate previous anatomy modules.

It imports and reuses:

- Phase 01 time anatomy
- Phase 02 reference field via later dependency chain
- Phase 03 hunt field via later dependency chain
- Phase 05 confirmation field directly

## Engine flow

```text
broker time
  -> closed-candle observation boundary
  -> New York trading-day snapshot
  -> CG cycle snapshots
  -> Phase 05 final states
  -> drawing output
  -> ledger output
  -> panel output
```

## Safety boundary

The engine has no order API usage and no risk/target logic.
