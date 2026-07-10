---
id: EXP0018-P01-02-DOMAIN-TIME-MODEL
title: "EXP0018 P01 — Domain Time Model"
type: specification
status: implemented-awaiting-metaeditor-compile
project: EXP0018
phase: P01
version: 2.2.0
created: 2026-07-10
updated: 2026-07-10
owner: Quant Engineering
tags:
  - exp0018
  - daye-trader
  - phase01
  - time-kernel
---


# مدل زمان

سه زمان نباید با هم مخلوط شوند:

```text
Broker Time  = شکل timestamp ورودی ترمینال
UTC Instant  = هویت مطلق و بدون ابهام لحظه
NY Wall Time = ساعت محلی مورد استفاده دکترین Daye
```

هویت event و period بر UTC ساخته می‌شود؛ نام‌گذاری و boundary بر NY Wall Time.

## سه زمان رخداد

- `event_time_utc`: زمان واقعی boundary؛
- `availability_time_utc`: نخستین زمانی که سیستم آن را مشاهده کرد؛
- `processing_time_utc`: زمان اجرای callback.

این جداسازی replay را causal نگه می‌دارد و تأخیر timer را با زمان واقعی boundary اشتباه نمی‌گیرد.

