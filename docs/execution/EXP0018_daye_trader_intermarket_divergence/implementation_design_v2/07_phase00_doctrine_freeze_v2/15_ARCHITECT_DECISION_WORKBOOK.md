---
id: EXP0018-P00-WORKBOOK
title: "EXP0018 Phase 00 — Architect Decision Workbook"
type: questionnaire
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

# برگه تصمیم معمار استراتژی

برای بسته‌شدن Phase 00، پاسخ هر مورد باید یکی از گزینه‌ها یا یک تعریف صریح جایگزین باشد.

## تصمیم‌های Critical

### DY-A01 — جهت

- گزینه A: `High-side = SELL`, `Low-side = BUY` **(پیشنهاد مهندسی)**
- گزینه B: `High-side = BUY`, `Low-side = SELL`
- گزینه C: Core بدون BUY/SELL و فقط HIGH/LOW؛ direction در فاز بعد

**پاسخ نهایی:** …

### DY-A02 — TWO

- گزینه A: Tuesday trading-day open = Monday 18:00 NY **(پیشنهاد)**
- گزینه B: Tuesday civil date 18:00 NY
- گزینه C: تعریف دیگر با مثال تاریخ دقیق

**پاسخ نهایی:** …

### DY-A03 — Weekly boundary

- گزینه A: Sunday 18:00 NY تا Friday 16:59:59 NY **(پیشنهاد فنی futures)**
- گزینه B: Monday 18:00 NY تا Friday 16:59:59
- گزینه C: broker weekly candle
- گزینه D: تعریف دیگر

**پاسخ نهایی:** …

### DY-A04 — First Sweep scope

- گزینه A: per relationship + reference period + side + hunter/protected **(پیشنهاد)**
- گزینه B: per reference period + side، مستقل از relationship
- گزینه C: فقط per exact current/reference pair
- گزینه D: تعریف دیگر

**پاسخ نهایی:** …

### DY-A05 — NP

- گزینه A: P فعلی در برابر N بلافاصله قبل در همان Trading Day **(پیشنهاد)**
- گزینه B: P قبلی در برابر N قبلی
- گزینه C: تعریف دیگر

**پاسخ نهایی:** …

### DY-A12 — خط تاریخی

- گزینه A: خط Confirmed همیشه در lookback باقی بماند **(پیشنهاد و مطابق Word)**
- گزینه B: پس از breach/retirement حذف شود
- گزینه C: فقط با input قابل انتخاب باشد

**پاسخ نهایی:** …

## تصمیم‌های Core Boundary

### DY-A06
Core فقط wick-touch باشد و body/close به P16 منتقل شود؟ **پیشنهاد: بله**

### DY-A07
۲۲ رابطه Core مستقل از taxonomy SSMT بمانند؟ **پیشنهاد: بله**

## تصمیم‌های Optional

### DY-A08
Extended True Opens در module/Expert جدا؟ **پیشنهاد: بله**

### DY-A09
DFR ابتدا research-only module؟ **پیشنهاد: بله**

### DY-A10
Triad در v1 فقط observer؟ **پیشنهاد: بله**

### DY-A11
News در v1 فقط ledger context و نه filter؟ **پیشنهاد: بله**

## تأیید نهایی

```text
Approved by:
Approval date:
Doctrine version:
Notes:
```
