# Phase 14 Module Architecture

## Dependency direction

```text
EXP0017 signal authority
        ↓
CGX_SignalSource
        ↓
CGX_SignalRegistry
        ↓
CGX_TradePlanner
  ├─ CGX_ClosedCandle
  ├─ CGX_EntryModel
  ├─ CGX_StopModel
  ├─ CGX_TargetModel
  │    ├─ CGX_TargetModelATR
  │    └─ CGX_TargetModelRiskMultiple
  └─ CGX_VolumeModel
        ↓
CGX_OrderRouter
        ↓
CGX_Audit
        ↓
CGX_ExecutionVisuals
```

`CGX_Engine` owns orchestration. The expert owns input declarations and configuration mapping.

## Extension seams

### Entry

Add entry implementations behind `ECGXEntryModel`; do not alter signal anatomy.

### Stop

Add stop implementations behind `ECGXStopModel`. Spread treatment belongs to stop geometry, not signal generation.

### Target

`CCGX_TargetModel` dispatches to dedicated providers. ATR and stop-risk multiple calculations remain isolated.

### Volume

All monetary sizing belongs to `CCGX_VolumeModel`. Broker step normalization and post-normalization risk verification are mandatory.

### Position policy

Hedge permission and position-count policy remain router concerns. They do not alter signal identity.

### Visuals

`CCGX_ExecutionVisuals` consumes accepted execution state only. It cannot create a signal or route an order and owns only `EXP0017_P14_` objects.

## Invariants

- Signal anatomy contains no `CTrade`.
- Entry models do not size volume.
- Stop models do not create targets.
- Target models do not access position state.
- Volume is normalized downward for risk-capped models.
- Rejected plans cannot reach `CTrade`.
- Hedge-off blocks opposite owned positions.
- Visuals are downstream of accepted execution.
- Paper mode cannot send orders.
- Backtest-only mode cannot send outside Strategy Tester.
