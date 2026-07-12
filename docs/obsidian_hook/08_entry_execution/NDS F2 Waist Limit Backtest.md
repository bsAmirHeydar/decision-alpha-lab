---
tags:
  - nds
  - f2
  - entry
  - backtest
status: implemented
---

# NDS F2 Waist Limit Backtest

## Contract

```text
Fresh confirmed F2
→ bullish Buy Limit below F2 waist
→ bearish Sell Limit above F2 waist
→ SL at canonical parent F1 waist
→ TP at F2 Leg2 endpoint
→ one exposure
```

## Authority

- [[NDS Entry Doctrine]]
- [[NDS Lightweight Backtest Runtime]]
- [[NDS F2 Fast Exact Backtest Runtime]]

## Separation

Hook is not an entry source and Hook scanning is disabled in the fast F2 executable. Phoenix node, F1 and F2 lifecycle modules remain authoritative.

## Code

- `mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2FastDetector.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh`
