---
tags:
  - nds
  - f2
  - backtest
  - performance
  - execution
status: implemented
---

# NDS F2 Fast Exact Backtest Runtime

## Contract

```text
newly observable confirmed F2
→ Buy Limit one tick below bullish F2 waist
→ Sell Limit one tick above bearish F2 waist
→ SL at parent F1 waist
→ TP at F2 Leg2
→ one exposure only
```

## Accuracy correction

The pivot timestamp of `F2.confirm` is not the time the setup becomes knowable. The runtime reconstructs the exact right-clearance completion bar and uses that as freshness authority.

## Performance boundary

- Hook scan disabled.
- F3 disabled.
- no `FP_DetectAllScales` global finalization.
- no renderer, CSV, timer, Print, timing statistics, terminal Global Variable registry or global mutex.
- detector skipped while a managed pending order or position exists.

## Code

- `mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2FastDetector.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh`

## Related

- [[NDS F2 Waist Limit Backtest]]
- [[NDS Lightweight Backtest Runtime]]
