---
tags:
  - nds
  - f2
  - waist-break
  - point-2
  - entry
  - backtest
status: canonical_execution_contract
---

# NDS F2 Waist Limit Backtest

## قرارداد صحیح

```text
فلگ دو لگ F2 کامل می‌شود
→ کمر F2 = شماره 1
→ Limit پشت کمر F2 قرار می‌گیرد
→ Fill شدن Limit = شماره 2
→ Stop پشت کمر F1 والد
→ Target انتهای دو لگ F2 / F2 Leg2
```

## نکته زمانی حیاتی

ورود منتظر Confirm شدن F2 نمی‌ماند. Confirm شدن F2 زمانی رخ می‌دهد که پس از شاخه waist-break، قیمت دوباره انتهای فلگ F2 را بزند. همان نقطه Target این ستاپ است.

پس:

```text
F2 body complete → سفارش مسلح
F2 confirmed → برای ورود دیر است
```

## Point 1 / Point 2

- `Point 1 = f2.waist`
- `Point 2 = first strict penetration beyond f2.waist`
- Limit یک یا چند Tick پشت کمر، نمایش اجرایی Point 2 است.

## جهت صعودی

```text
Buy Limit = F2 Waist - entry ticks
SL = F1 Waist - stop ticks
TP = F2 Leg2
```

## جهت نزولی

```text
Sell Limit = F2 Waist + entry ticks
SL = F1 Waist + stop ticks
TP = F2 Leg2
```

## استقلال

این ستاپ از Hook، Zone، CG و AI برای مجوز ورود استفاده نمی‌کند.

## کد

- `mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2FastDetector.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh`

## اسناد

- [[../../nds_entry_architecture/f2_waist_break_point2_limit/README|F2 Waist-Break Point-2 detailed package]]
- [[NDS F2 Fast Exact Backtest Runtime]]
