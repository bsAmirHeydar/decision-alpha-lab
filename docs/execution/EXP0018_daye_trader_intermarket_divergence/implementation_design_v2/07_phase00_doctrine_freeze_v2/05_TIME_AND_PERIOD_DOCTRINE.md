---
id: EXP0018-P00-TIME
title: "EXP0018 Phase 00 — Time and Period Doctrine"
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

# دکترین زمان و Period

## Clock رسمی

تمام زمان‌ها در domain با New York local time تعریف می‌شوند. تبدیل پیشنهادی:

```text
Broker timestamp → UTC → New York local timestamp
```

DST باید با policy مشخص و test boundary پوشش داده شود. ذخیره identity باید ambiguity ساعت‌های DST را تحمل کند و صرفاً به نمایش رشته‌ای وابسته نباشد.

## Trading Day

```text
Start: 18:00:00 NY
End:   16:59:59 NY next civil date
Gap:   17:00:00–17:59:59
```

## Sessionها

| ID | Start | End |
|---|---:|---:|
| A | 18:00:00 | 23:59:59 |
| L | 00:00:00 | 05:59:59 |
| N | 06:00:00 | 11:59:59 |
| P | 12:00:00 | 16:59:59 |

## زیرسایکل‌ها

| A | L | N | P |
|---|---|---|---|
| a1 18:00–19:29:59 | l1 00:00–01:29:59 | n1 06:00–07:29:59 | p1 12:00–13:29:59 |
| a2 19:30–20:59:59 | l2 01:30–02:59:59 | n2 07:30–08:59:59 | p2 13:30–14:59:59 |
| a3 21:00–22:29:59 | l3 03:00–04:29:59 | n3 09:00–10:29:59 | p3 15:00–16:29:59 |
| a4 22:30–23:59:59 | l4 04:30–05:59:59 | n4 10:30–11:59:59 | p4 16:30–16:59:59 |

`p4` عمداً ۳۰ دقیقه است و نباید برای هم‌شکل‌شدن با بقیه کش داده شود.

## Daily

Daily Period همان Trading Day بالا است، نه کندل تقویمی broker.

## Weekly

مرز Weekly تا تصویب ADR-DY-A03 blocker است. Registry می‌تواند نوع `W` را بشناسد اما WW نباید فعال شود تا boundary تصویب و fixture شود.

## TWO/TDO

- TDO کاندید پایه: Open ساعت 00:00 NY تا 16:59:59 همان روز.
- TWO کاندید پایه: Tuesday trading-day open که در futures labeling معمولاً Monday 18:00 NY است؛ تصمیم نهایی ADR-DY-A02.

## Invariantها

- هیچ Period با bar index تعریف نمی‌شود؛ identity براساس زمان canonical است.
- bar کم/زیاد، weekend و expiry نباید boundary را تغییر دهد.
- Period ناقص `INCOMPLETE` است؛ نباید به‌عنوان OHLC کامل استفاده شود.
