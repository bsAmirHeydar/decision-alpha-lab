# EXP0017 Phase 14 — Modular Raw Execution Backtest

Phase 14 adds the first order-producing expert for the EXP0017 cycle-group divergence engine.

The signal authority remains the Hotfix011 confirmation stack. Phase 14 consumes `SCGCFinalSignal` and does not redefine reference freshness, hunt asymmetry, protected-reference retirement, or closed-candle confirmation.

## Owner-approved execution profile

- Entry: market order on the first available tick after the confirmation candle closes.
- Trade leg: input-selectable protected symbol or hunter symbol.
- Default trade leg: protected symbol (`signal.clean_symbol`).
- Stop: behind the selected trade symbol's confirmation candle.
- Buy stop: confirmation candle low minus optional point buffer.
- Sell stop: confirmation candle high plus optional point buffer.
- Target: ATR multiple measured from planned market entry.
- Default ATR: Wilder ATR, period 14, multiplier 1.0.
- Default sizing: 1% equity risk, normalized down to broker volume step.
- Default enabled cycle group: `cg_3m` only.
- All other 20 CG trade switches exist and default to disabled.
- Default runtime: Strategy Tester only. The expert refuses to transport orders outside the tester unless the runtime input is explicitly changed.

## Implementation

### Expert

- `mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Raw_Execution_Backtest.mq5`

### Execution modules

- `CGX_Types.mqh`
- `CGX_Utilities.mqh`
- `CGX_SignalSource.mqh`
- `CGX_ClosedCandle.mqh`
- `CGX_EntryModel.mqh`
- `CGX_StopModel.mqh`
- `CGX_TargetModelATR.mqh`
- `CGX_VolumeModel.mqh`
- `CGX_TradePlanner.mqh`
- `CGX_SignalRegistry.mqh`
- `CGX_OrderRouter.mqh`
- `CGX_Audit.mqh`
- `CGX_Engine.mqh`

## Phase boundary

This phase produces broker/tester orders and a structured audit CSV. It does not rank CGs, apply AI filters, optimize parameters, or alter divergence doctrine.

## Related documents

- [[PHASE14_EXECUTION_CONTRACT]]
- [[PHASE14_MODULE_ARCHITECTURE]]
- [[PHASE14_BACKTEST_OPERATOR_GUIDE]]
- [[PHASE14_VALIDATION_PLAN]]
