# Shared-Core Parity Contract

Performance isolation must not create a second trading algorithm.

## Hook core

`FP_HookPhase02DetectionCore.mqh` owns the pure Hook Phase 02 process:

```text
Phase 01 node build
→ Hook sequence build
→ F3 ownership annotation
→ NDS structure snapshot
→ report finalization
```

The production `FP_HookPhase02Engine.mqh` wraps this core and adds optional drawing, CSV, and logs. The backtest executable calls the core directly.

## Trade core

`FP_NDSHookTradeExecutionCore.mqh` owns the complete executable state machine. It contains the exact workflow previously embedded in `FP_NDSHookTradeEngine.mqh`.

The production wrapper adds the CSV sink. The lightweight backtest calls the same core without the sink.

## Parity boundary

Rule parity means identical functions and configuration values. Runtime-profile parity additionally requires the `PARITY` profile, which uses the original 5,000-bar and eight-scale context. The default `FAST` profile uses the same rules over a bounded 1,200-bar/four-scale context and may therefore differ where an older or larger-scale parent structure is required.
