---
id: EXP0018-P00-SCENARIOS
title: "EXP0018 Phase 00 — Positive and Negative Scenarios"
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

# سناریوهای مثبت و منفی

## S-01 — High-side one-sided hunt

- Reference high برای A و B موجود است.
- A سطح خودش را لمس می‌کند.
- B سطح خودش را لمس نمی‌کند.
- تا Close میزبان وضعیت حفظ می‌شود.

انتظار: `CONFIRMED_SIDE_HIGH`, Hunter=A, Protected=B.

## S-02 — Low-side one-sided hunt

همان ساختار برای Low. انتظار: `CONFIRMED_SIDE_LOW`.

## S-03 — Equality

current high دقیقاً برابر reference high است. انتظار: Hunt=true.

## S-04 — Double Hunt intrabar

A اول Hunt می‌کند و B قبل از Close Hunt می‌کند. انتظار: no confirmed line.

## S-05 — Candidate disappears

در این مدل touch برگشت‌پذیر نیست؛ اگر touch رخ داده، observation حفظ می‌شود. فقط one-sided بودن با Hunt نماد دوم تغییر می‌کند.

## S-06 — Missing symbol B

A داده کامل و Hunt دارد؛ B داده ندارد. انتظار: `UNAVAILABLE_DATA`, نه divergence.

## S-07 — Multiple relationships same close

LN و n2n3 هم‌زمان معتبرند. انتظار: دو event مستقل.

## S-08 — Same relationship both sides

High-side و Low-side هر دو ممکن است برای referenceهای مستقل در یک Close رخ دهند. هیچ suppression عمومی بدون doctrine مجاز نیست.

## S-09 — First sweep duplicate

همان opportunity key در callback دوم دیده می‌شود. انتظار: no second event.

## S-10 — Protected later breaches

بعد از confirmation، Protected همان reference-side خود را Hunt می‌کند. انتظار: lifecycle retire برای future opportunity؛ historical line طبق ADR-DY-A12 باقی می‌ماند.

## S-11 — Expiry short history

فقط یک روز تاریخ موجود است. انتظار: محاسبه فقط از اولین رابطه قابل پشتیبانی؛ no crash/no invented period.

## S-12 — Cross-symbol scale protection

قیمت NDX نباید روی chart SPX coordinate شود. انتظار: renderer فقط symbol-local values.
