---
type: contract
system: NDS
phase: 55
status: implemented
---

# NDS Backtest Parity Contract

There is one Hook algorithm and one executable trade state machine.

## Shared Hook core

`FP_HookPhase02DetectionCore.mqh`

## Shared execution core

`FP_NDSHookTradeExecutionCore.mqh`

Production wrappers add rendering/export. The backtest path adds neither.

## Acceptance

- use `PARITY` with `InpBTExactAcceleration=true` for maximum exact speed;
- repeat the same run with `InpBTExactAcceleration=false` as the full scheduling oracle;
- keep symbol, timeframe, interval, tick model and every other input identical;
- use `FAST` only when bounded context is intentionally acceptable;
- do not compare chart objects or CSV outputs because the lightweight runtime deliberately has none.

## Related

- [[NDS Lightweight Backtest Runtime]]
- [[NDS Hook Trade State Machine]]

- [[NDS Hook 86.4 Exact Acceleration]]
