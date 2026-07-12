---
tags:
  - nds
  - f2
  - backtest
  - performance
  - execution
status: corrected
---

# NDS F2 Fast Exact Backtest Runtime

## Corrected contract

```text
newly observable complete unconfirmed F2 body
→ F2 Waist = Point 1
→ Buy Limit below bullish F2 Waist / Sell Limit above bearish F2 Waist
→ fill = executable Point 2
→ SL behind direct parent F1 Waist
→ TP at F2 Leg2 endpoint
→ one exposure only
```

## Accuracy correction

Freshness is measured from the exact bar where the F2 Leg2 node becomes observable. `F2.confirm` is deliberately excluded because it is the target event, not the setup-availability event.

## Performance boundary

- no Hook branch construction;
- F3 disabled;
- no global ownership/canonical-render finalization;
- no renderer, CSV, timer, custom Print, timing statistics, terminal Global Variable registry or global mutex;
- detector skipped while a position is open;
- only a one-bar target-consumption check runs while a pending order exists.

## Code

- `mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2FastDetector.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh`

## Related

- [[NDS F2 Waist-Break Point2 Limit Setup]]
- [[NDS F2 Waist Limit Backtest]]
- [[NDS Lightweight Backtest Runtime]]
