---
id: EXP0018-P03-IDENTITY
title: "P03 Period Entity and Identity"
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

# موجودیت و هویت دوره

هویت اصلی دوره از P01 می‌آید:

```text
EXP0018|<FAMILY>|<CODE>|<START_UTC_EPOCH>
```

هویت Snapshot نماد:

```text
EXP0018|P03|SYMBOL|<PERIOD_INSTANCE_ID>|<CANONICAL_SYMBOL>
```

هویت Paired Period:

```text
EXP0018|P03|PAIR|<PERIOD_INSTANCE_ID>|<SYMBOL_A>|<SYMBOL_B>
```

قیمت یا bar index در identity استفاده نمی‌شود. این جداسازی اجازه می‌دهد OHLC بعد از کامل‌شدن دوره تغییرناپذیر شود، در حالی که ID ثابت می‌ماند.
