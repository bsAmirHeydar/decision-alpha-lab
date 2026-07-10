---
id: EXP0018-P00-DATA
title: "EXP0018 Phase 00 — Data and Partial History Doctrine"
type: specification
status: draft
project: EXP0018
version: 2.1.0
created: 2026-07-10
updated: 2026-07-10
owner: Strategy Architect
tags:
  - exp0018
  - daye-trader
  - phase00
  - doctrine-freeze
---

# دکترین داده، تاریخ ناقص و expiry

## وضعیت داده

هر درخواست داده یکی از وضعیت‌های زیر را برمی‌گرداند:

```text
COMPLETE
PARTIAL
UNAVAILABLE
UNSYNCHRONIZED
OUT_OF_RANGE
```

## قواعد

- `CopyRates` failure باید ثبت شود.
- `SymbolSelect` و sync history باید بررسی شوند.
- alignment فقط با timestamp canonical انجام می‌شود.
- forward-fill قیمت یا ساخت bar مصنوعی ممنوع است.
- شنبه/یکشنبه بدون bar نباید به‌عنوان Period خالی اجباری تولید شوند.
- در ابتدای expiry اگر تاریخ کافی وجود ندارد، موتور تا اولین بازه قابل محاسبه عقب‌نشینی می‌کند؛ نباید crash یا reference جعلی بسازد.
- اگر یکی از دو نماد داده ندارد، signal status `UNAVAILABLE` است.
- replay و live باید برای داده یکسان event یکسان بسازند.

## Bounded work

- lookback هفته‌ها input محدود دارد؛
- full-history rescan روی هر tick ممنوع است؛
- cache invalidation فقط با بسته‌شدن bar/period یا تغییر config انجام می‌شود.
