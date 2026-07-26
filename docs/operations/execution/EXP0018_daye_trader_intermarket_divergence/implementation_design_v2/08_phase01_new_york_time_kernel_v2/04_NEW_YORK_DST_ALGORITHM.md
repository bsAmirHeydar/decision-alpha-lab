---
id: EXP0018-P01-04-NEW-YORK-DST-ALGORITHM
title: "EXP0018 P01 — New York DST Algorithm"
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


# الگوریتم DST

در حالت خودکار:

- شروع: یکشنبه دوم مارس، 02:00 EST = 07:00 UTC؛
- پایان: یکشنبه اول نوامبر، 02:00 EDT = 06:00 UTC؛
- تابستان: UTC-4؛
- زمستان: UTC-5.

## Spring Gap

در شروع DST، ساعت‌های 02:00 تا 02:59 محلی وجود ندارند. Local→UTC برای این بازه `NONEXISTENT_LOCAL_TIME` می‌دهد.

## Fall Fold

در پایان DST، ساعت 01:00 تا 01:59 دو بار رخ می‌دهد. UTC→NY همیشه قطعی است و `fold=0/1` را نگه می‌دارد. برای period start از earliest UTC و برای period end از latest UTC استفاده می‌شود تا پنجره wall-clock کامل پوشش داده شود.

## اثر روی طول واقعی period

پنجره‌ها با ساعت دیواری نیویورک تعریف شده‌اند. در شب DST، elapsed UTC یک period ممکن است با nominal minutes فرق داشته باشد. این اختلاف خطا نیست؛ با `is_dst_variable_duration=true` ثبت می‌شود.

