---
id: EXP0018-P01-03-BROKER-TO-UTC-ADAPTER
title: "EXP0018 P01 — Broker to UTC Adapter"
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


# تبدیل Broker به UTC

## حالت canonical

`MANUAL_FIXED` برای backtest و replay canonical است. offset باید مطابق timestamp تاریخچه همان بروکر تنظیم شود.

```text
UTC = Broker Time - Broker UTC Offset
```

## حالت Auto Current Live

این حالت اختلاف `TimeTradeServer()` و `TimeGMT()` را در لحظه فعلی می‌سنجد. برای historical replay امن نیست؛ snapshot با `is_replay_safe=false` علامت می‌خورد.

## چرا offset پنهانی تشخیص داده نمی‌شود؟

بروکرها می‌توانند DST یا schedule اختصاصی داشته باشند. استفاده از offset امروز برای تاریخ قدیمی، خطای ساکت می‌سازد. به همین دلیل حالت manual پیش‌فرض است.

