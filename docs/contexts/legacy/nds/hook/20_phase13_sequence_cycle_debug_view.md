# Phase 13 — Sequence + Cycle Arc Debug View

## هدف

این فاز برای وقتی است که خروجی رسمی Hook هنوز از نظر بصری شلوغ است و باید دقیقاً دیده شود که موتور Hook چطور sequence را می‌شمارد.

تمرکز این فاز روی این‌هاست:

- Origin هر CycleHook
- X1 / X2 / X3 / X4
- خط اتصال Xها
- شماره sequence
- تعداد Xهای همان sequence
- نیم‌دایره‌ی Cycle روی بازه‌ی همان sequence

این فاز عمداً P05/P06 quality/type labelها، thresholdها، projectionها، و labelهای debug سنگین را خاموش می‌کند.

## View Profile جدید

```text
FP_HOOK_P07_VIEW_SEQUENCE_CYCLE_DEBUG
```

این پروفایل فقط Phase 02 را به‌عنوان سطح اصلی نمایش فعال می‌کند:

- `draw_origin = true`
- `draw_x_nodes = true`
- `draw_x_lines = true`
- `draw_cycle_arc = true`
- `draw_sequence_count_label = true`

و این‌ها را خاموش می‌کند:

- Phase 03 Y overlays
- Phase 04 threshold / ND / death overlays
- Phase 05 type labels
- Phase 06 quality labels

## Inputهای جدید Phase 02

```text
InpHookPhase02DrawCycleArc
InpHookPhase02DrawSequenceCountLabel
InpHookPhase02CycleArcSegments
InpHookPhase02CycleArcHeightRatio
InpHookPhase02CycleArcColor
InpHookPhase02SequenceCountLabelColor
```

## منطق نیم‌دایره

Arc از `Origin` تا آخرین X معتبر sequence رسم می‌شود.

- برای sequence مثبت، arc پایین ساختار رسم می‌شود.
- برای sequence منفی، arc بالای ساختار رسم می‌شود.
- ارتفاع arc بر اساس فاصله‌ی قیمتی origin تا آخرین X و `CycleArcHeightRatio` محاسبه می‌شود.
- arc با قطعه‌های trend line ساخته می‌شود تا در MQL5 پایدار و قابل پاک‌سازی باشد.

## Recommended inputs

برای دیدن دقیق محاسبات sequence:

```text
InpNDSHookDisplayFamily = FP_NDS_HOOK_DISPLAY_HOOK_ONLY
InpHookPhase07ViewProfile = FP_HOOK_P07_VIEW_SEQUENCE_CYCLE_DEBUG
InpHookPhase07ShowLabels = false
InpHookPhase07CleanBeforeApply = true
InpHookPhase07MaxSequencesToDraw = 8
InpHookPhase02DrawCycleArc = true
InpHookPhase02DrawSequenceCountLabel = true
```
