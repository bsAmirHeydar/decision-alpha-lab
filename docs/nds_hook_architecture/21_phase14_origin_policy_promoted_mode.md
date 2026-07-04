# Phase 14 — Hook Origin Policy / Promoted Origin Mode

## هدف

قبل از Inspector، منطق مبدا Hook باید دوحالته شود. مشکل قبلی این بود که در حالت fixed هر نود هم‌جهت، مخصوصاً در scaleهای کوچک مثل L2، می‌توانست origin مستقل شود و تعداد Hookهای هم‌پوشان زیاد می‌شد.

## Input جدید

```text
InpHookPhase02OriginPolicy
```

حالت‌ها:

```text
FP_HOOK_P02_ORIGIN_FIXED_EVERY_NODE
FP_HOOK_P02_ORIGIN_PROMOTE_WITH_INTERNAL_X
```

## حالت ۱ — Fixed Every Node

همان رفتار قبلی است:

- هر نود واجد شرایط می‌تواند origin شود.
- origin تا انتهای sequence ثابت می‌ماند.
- برای debug کامل همه candidateها مفید است.
- روی چارت بسیار شلوغ می‌شود.

## حالت ۲ — Promote With Internal X

این حالت برای خواندن تمیزتر Hook اضافه شد:

- sequence به‌صورت rolling window ساخته می‌شود.
- وقتی داخل Hook تعداد Xها از ظرفیت `max_x_nodes_per_sequence` عبور کند، origin به جلو promote می‌شود.
- یعنی origin قدیمی دیگر origin Hook فعلی نیست.
- مبدا جدید از X1 قبلی ساخته می‌شود و Xها یک خانه به جلو شیفت می‌شوند.

مثال مفهومی:

```text
O -> X1 -> X2 -> X3 -> X4
```

اگر X جدید بیاید:

```text
old: O  -> X1 -> X2 -> X3 -> X4
new: X1 -> X2 -> X3 -> X4 -> X5
```

در ساختار محدود فعلی، `X1` قدیمی origin جدید می‌شود و آخرین X جدید در آخرین slot قرار می‌گیرد.

## نتیجه عملی

این حالت تعداد originهای قدیمی و هم‌پوشان را کم می‌کند و برای Inspector / Sequence Cycle Debug مناسب‌تر است.

## Default جدید

برای Hook debug، default روی promoted mode گذاشته شد:

```text
InpHookPhase02OriginPolicy = FP_HOOK_P02_ORIGIN_PROMOTE_WITH_INTERNAL_X
```

برای برگشت به رفتار قبلی:

```text
InpHookPhase02OriginPolicy = FP_HOOK_P02_ORIGIN_FIXED_EVERY_NODE
```
