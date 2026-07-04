# Phase 15 — Hard Sequence Lens Cleanup

## هدف

بعد از اضافه شدن نیم‌دایره‌ی Cycle و حالت promoted origin، هنوز ممکن بود روی چارت آبجکت‌های قدیمی P05/P06 یا رندر اصلی Rally باقی بمانند. دلیل عملی این بود که MT5 مقدار inputهای قبلی را روی instance چارت نگه می‌دارد و بعضی overlayها قبل از reset کامل دوباره روی چارت دیده می‌شدند.

این فاز حالت `SEQUENCE_CYCLE_DEBUG` را از یک view معمولی به یک hard inspector lens تبدیل می‌کند.

## رفتار جدید در `FP_HOOK_P07_VIEW_SEQUENCE_CYCLE_DEBUG`

- Phase 01 فقط برای ساخت داده‌ی نود استفاده می‌شود و چیزی رسم نمی‌کند.
- Phase 02 تنها لایه‌ی قابل نمایش است.
- Phase 03، Phase 04، Phase 05 و Phase 06 از نظر runtime disabled می‌شوند، نه فقط draw=false.
- تعداد sequence قابل رسم به‌صورت hard cap روی 1 قرار می‌گیرد.
- P03/P04/P05/P06 نمی‌توانند label یا marker جدید تولید کنند.
- قبل از هر run، آبجکت‌های خانواده‌ی Hook و آبجکت‌های رندر اصلی با prefixهای input پاک می‌شوند.
- حتی اگر `CleanBeforeApply=false` از تنظیمات قدیمی MT5 باقی مانده باشد، sequence lens cleanup اجباری اجرا می‌شود.

## نتیجه

روی چارت باید فقط این‌ها بماند:

```text
O
X1 / X2 / X3 / X4
X-lines
Cycle semicircle
یک label کوتاه sequence مثل C928 L5 X3 n=4
```

و این‌ها نباید دوباره دیده شوند:

```text
P05 ...
P06 ...
ORIGIN/DEATH
X CLOSE 50%
H01 PEAK / H01 VALLEY
ND TH
```

## Recommended inputs

```text
InpHookPhase07ViewProfile = FP_HOOK_P07_VIEW_SEQUENCE_CYCLE_DEBUG
InpHookPhase02OriginPolicy = FP_HOOK_P02_ORIGIN_PROMOTE_WITH_INTERNAL_X
InpHookPhase07MaxSequencesToDraw = 1
```

در این profile، حتی اگر مقدار max در MT5 قدیمی‌تر باشد، کد آن را به 1 محدود می‌کند.
