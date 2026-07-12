---
tags:
  - nds
  - f2
  - canonical-setup
  - waist-break
  - point-1
  - point-2
status: canonical
---

# NDS F2 Waist-Break Point2 Limit Setup

## Canon

> وقتی فلگ دو لگ F2 کامل شد، کمر همان فلگ شماره 1 است. اولین عبور سخت از پشت کمر، شماره 2 است. سفارش Limit از قبل پشت کمر F2 قرار می‌گیرد تا Fill آن همان ورود روی شماره 2 باشد. استاپ پشت کمر F1 والد و تارگت انتهای دو لگ F2 است.

## State flow

```text
F1 confirmed
→ F2 Origin-Leg1-Waist-Leg2 complete
→ arm pending behind F2 Waist
→ fill = Point 2
→ SL behind F1 Waist
→ TP at F2 Leg2
```

## Forbidden reinterpretations

- Confirmed F2 is not the trigger.
- F2 Waist itself is not Point 2.
- `f2.confirm` is not the target field.
- Hook is not an entry authority.
- No market chase after missed limit.

## Authority

- [[NDS F2 Waist Limit Backtest]]
- [[../../nds_entry_architecture/f2_waist_break_point2_limit/01_canonical_setup_contract|Canonical setup contract]]
- [[../../nds_entry_architecture/f2_waist_break_point2_limit/02_structural_anatomy|Structural anatomy]]
- [[../../nds_entry_architecture/f2_waist_break_point2_limit/03_execution_state_machine|Execution state machine]]

## Portfolio extension

```text
RR = abs(Target - Entry) / abs(Entry - Stop)
Default minimum RR = 1.0
Opposite-direction hedge contexts = enabled
Same-direction distinct contexts = enabled
```

The deterministic F2 body-version hash is the context authority. The same hash cannot submit twice. Parallel same-symbol positions require an MT5 hedging account.

- [[NDS F2 RR Hedge and Parallel Contexts]]
