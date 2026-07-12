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
Confirmed F2
→ bullish limit below F2 waist / bearish limit above F2 waist
→ SL at canonical parent F1 waist
→ TP at F2 Leg2 endpoint
→ one exposure
```

## Authority

- [[NDS Entry Doctrine]]
- [[NDS Lightweight Backtest Runtime]]

## Important separation

Hook is not an entry source for this profile. Phoenix may still use internal phase-boundary evidence while constructing canonical F1/F2, but the order layer receives only F2 and its canonical parent F1.

## Code

- `mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh`
