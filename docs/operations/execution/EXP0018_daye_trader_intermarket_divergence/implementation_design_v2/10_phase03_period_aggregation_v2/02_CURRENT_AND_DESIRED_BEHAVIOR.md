---
id: EXP0018-P03-BEHAVIOR
title: "P03 Current and Desired Behavior"
type: spec
status: active
project: EXP0018
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - phase03
  - period-aggregation
---

# رفتار فعلی و مطلوب

قبل از P03، سیستم فقط barهای هم‌زمان دو نماد را می‌شناسد. هنوز مفهوم «سشن N روز 2026-07-10» یا «زیرسایکل n3» به‌صورت یک شیء OHLC مستقل وجود ندارد.

رفتار مطلوب این است که برای هر دوره یک identity پایدار ساخته شود، barهای هر نماد فقط در Window همان دوره جمع شوند و وضعیت کامل‌بودن به‌صورت typed باقی بماند. اولین دوره داخل lookback معمولاً ناقص است و نباید به‌دلیل وجود چند bar، کامل فرض شود. دوره جاری نیز `OPEN` است، نه `PARTIAL` و نه `COMPLETE`.
