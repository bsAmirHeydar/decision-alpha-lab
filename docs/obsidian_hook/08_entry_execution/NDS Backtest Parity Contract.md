---
type: contract
system: NDS
phase: 53
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

- use `PARITY` for decision-by-decision comparison;
- use `FAST` for throughput;
- do not compare chart objects or CSV outputs because the lightweight runtime deliberately has none.

## Related

- [[NDS Lightweight Backtest Runtime]]
- [[NDS Hook Trade State Machine]]
