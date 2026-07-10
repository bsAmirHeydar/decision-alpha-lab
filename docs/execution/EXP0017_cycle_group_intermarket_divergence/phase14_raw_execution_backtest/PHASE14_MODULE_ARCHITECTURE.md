# Phase 14 Module Architecture

## Dependency direction

```text
Hotfix011 signal anatomy
        ↓
CGX_SignalSource
        ↓
CGX_SignalRegistry
        ↓
CGX_TradePlanner
  ├─ CGX_ClosedCandle
  ├─ CGX_EntryModel
  ├─ CGX_StopModel
  ├─ CGX_TargetModelATR
  └─ CGX_VolumeModel
        ↓
CGX_OrderRouter
        ↓
CGX_Audit
```

`CGX_Engine` owns orchestration only. The expert file owns input declarations and configuration mapping only.

## Extension seams

### New entry model

Add a new `ECGXEntryModel` value and implement it in `CCGX_EntryModel`. Do not change the divergence detector.

### New stop model

Add a new `ECGXStopModel` value and implement it in `CCGX_StopModel`. The selected stop must still pass planner geometry and volume sizing.

### New target model

Add a new `ECGXTargetModel` value and a dedicated target provider. Do not mix target calculations with the broker router.

### New volume model

Add a new `ECGXVolumeModel` value and implement sizing in `CCGX_VolumeModel`. Broker normalization remains mandatory.

### New execution leg

Trade-leg selection is isolated from divergence classification. Protected/hunter selection changes only `trade_symbol`; it does not mutate signal direction or source evidence.

## Invariants

- Signal anatomy does not know about CTrade.
- Entry models do not calculate risk volume.
- Stop models do not calculate ATR targets.
- The order router cannot invent missing geometry.
- Rejected plans cannot reach CTrade.
- Paper mode cannot send orders.
- Backtest-only mode cannot send outside Strategy Tester.
- The EA does not process the open confirmation candle.
