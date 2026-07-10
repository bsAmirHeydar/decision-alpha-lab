---
id: EXP0018-P03-INDEX
title: "EXP0018 P03 — Period Aggregation v2 Index"
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

# Phase 03 — Period Aggregation and Completeness v2

این فاز داده‌های بسته و symbol-local فاز ۲ را به Snapshotهای مستقل Daily، Session و Subcycle تبدیل می‌کند. خروجی آن برای هر نماد OHLC، تعداد bar موردانتظار و مشاهده‌شده، میزان پوشش، وضعیت `OPEN/PARTIAL/COMPLETE` و لینک دوره قبلی را نگه می‌دارد. سپس دو Snapshot هم‌هویت را بدون مخلوط‌کردن مقیاس قیمت در یک Paired Period قرار می‌دهد.

## ترتیب مطالعه

1. [[01_SCOPE_AND_AUTHORITY]]
2. [[03_PERIOD_ENTITY_AND_IDENTITY]]
3. [[05_COMPLETENESS_STATE_MODEL]]
4. [[07_SYMBOL_LOCAL_AGGREGATION_ALGORITHM]]
5. [[08_PAIRED_PERIOD_STORE]]
6. [[15_TEST_AND_FIXTURE_PLAN]]
7. [[21_HANDOFF_TO_P04_P05_P09_P11]]

## فایل اجرایی

`mql5/Experts/DayeTrader/EXP0018_Daye_Period_Anatomy.mq5`
