---
id: EXP0018-P00-DRAWING
title: "EXP0018 Phase 00 — Drawing and Persistence Doctrine"
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

# دکترین رسم و ماندگاری

## تنها زبان تصویری Core

```text
OBJ_TREND
```

خط از reference extreme روی چارت Hunter تا extreme اولین کندل تأییدشده روی همان چارت رسم می‌شود.

### High-side

```text
reference_high(hunter) → confirmation_bar_high(hunter)
```

### Low-side

```text
reference_low(hunter) → confirmation_bar_low(hunter)
```

## محل رسم

- فقط روی chart همان Hunter symbol؛
- فقط با price coordinate همان symbol؛
- اگر chart نماد موجود نیست، policy بازکردن یا عدم رسم باید explicit باشد؛ truth در ledger باقی می‌ماند.

## Label

- WW, DD, PA, AL, LN, NP: label وسط خط؛
- 16 رابطه کوچک: بدون label؛
- Comment panel و متن‌های اضافی جزء Core نیستند.

## Object identity

Object name باید deterministic و از stable IDs ساخته شود:

```text
EXP0018_DAYE_<relationship>_<side>_<reference-id>_<confirm-close>_<hunter>
```

## Persistence

منبع اصلی صریحاً می‌گوید خطوط تأییدشده حذف نشوند. پیشنهاد ADR-DY-A12 این است که retirement آینده فقط ساخت سیگنال جدید را ببندد و line historical را حفظ کند.

## Cleanup

پاک‌سازی فقط با prefix مالک EXP0018 مجاز است. حذف گسترده objectهای کاربر یا پروژه دیگر ممنوع است.
