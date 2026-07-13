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

> Phoenix تعریف کامل F2 را از قبل دارد: بدنه دو‌لگ، اصلاح پس از فلگ با حداقل ۱/۲، و سپس برگشت به انتهای فلگ برای تأیید F2. این ستاپ فقط ورود شاخه Waist-break را اجرا می‌کند: کمر بدنه فلگ F2 نقش Point 1 شاخه را دارد و سفارش Limit از قبل با عبور سخت و epsilon-safe پشت همان کمر قرار می‌گیرد تا Fill آن Point 2 اجرایی باشد. استاپ پشت کمر F1 والد و مرجع RR/تارگت ثابت انتهای فلگ F2 است.

## State flow

```text
F1 confirmed
→ Phoenix builds F2 flag body: Origin-Leg1-Waist-Leg2
→ execution adapter arms strict pending beyond F2 Waist
→ post-flag correction reaches Waist
→ fill = executable Waist-break Point 2
→ Phoenix continues its own post-flag count
→ favorable return to original Leg2 confirms F2
→ SL behind F1 Waist / fixed TP at original Leg2
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

- [[NDS F2 Canonical Point-2 Projection Root Fix]]
