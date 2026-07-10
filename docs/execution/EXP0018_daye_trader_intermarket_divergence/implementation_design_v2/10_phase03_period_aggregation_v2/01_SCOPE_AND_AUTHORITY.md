---
id: EXP0018-P03-SCOPE
title: "P03 Scope and Authority"
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

# دامنه و اختیار

P03 فقط مالک **ساخت دوره و بیان کامل‌بودن داده آن دوره** است. این فاز حق ندارد از High/Low نتیجه Hunt بگیرد، رابطه‌های ۲۲گانه را resolve کند، divergence بسازد یا روی چارت خط بکشد.

## ورودی authoritative

- `DAYE_TimeConfig` و `DAYE_PeriodRegistry` از P01
- `DAYE_SymbolBar` و exact timestamp alignment از P02
- فقط barهای بسته و اعتبارسنجی‌شده

## خروجی authoritative

- `DAYE_SymbolPeriodSnapshot`
- `DAYE_PairedPeriodSnapshot`
- `DAYE_PeriodStoreSummary`
- eventهای دوره

## Non-goals

Weekly تا پذیرش ADR-DY-A03 فعال نمی‌شود. True Open توسعه‌یافته، DFR، SSMT، News و Execution خارج از دامنه‌اند.
