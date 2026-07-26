---
id: EXP0018-P03-GRID-DST
title: "P03 Expected Grid and DST"
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

# Grid موردانتظار و DST

تعداد bar موردانتظار از UTC Window واقعی محاسبه می‌شود:

```text
expected = (end_utc - start_utc) / base_bar_seconds
```

به همین دلیل Daily در روز معمولی M1 برابر 1380 bar است، اما در روز Spring DST ممکن است 1320 و در Fall DST برابر 1440 باشد. اختلاف با nominal duration خطا نیست؛ نتیجه تبدیل ساعت دیواری نیویورک به UTC است.

Base timeframe باید ۳۰ دقیقه را دقیق تقسیم کند. این محدودیت تمام boundaryهای نیم‌ساعته و p4 را بدون bar شکسته پوشش می‌دهد.
