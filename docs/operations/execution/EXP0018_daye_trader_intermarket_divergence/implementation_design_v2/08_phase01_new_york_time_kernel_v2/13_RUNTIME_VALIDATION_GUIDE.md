---
id: EXP0018-P01-13-RUNTIME-VALIDATION-GUIDE
title: "EXP0018 P01 — Runtime Validation Guide"
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


# بررسی روی MT5

1. Expert را compile کن.
2. روی هر چارت عادی attach کن؛ symbol اهمیتی ندارد چون P01 market data نمی‌خواند.
3. `InpBrokerUtcOffsetHours` را مطابق server تنظیم کن.
4. Experts tab باید `embedded self-tests PASS` نشان دهد.
5. در 18:00 NY باید Trading Day و A/a1 تغییر کند.
6. از 17:00 تا 17:59 باید Gap=1 و Session/Subcycle=NONE باشد.
7. در 16:30 باید p4 شروع شود.
8. Chart Comment پیش‌فرض خاموش است.

برای audit، `InpWriteAuditCsv=true` را روشن کن. فایل در Common Files ساخته می‌شود.

