---
id: EXP0018-P01-01-SCOPE-AND-BOUNDARY
title: "EXP0018 P01 — Scope and Boundary"
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


# دامنه

P01 فقط این پرسش را جواب می‌دهد: «این لحظه مطلق در ساعت نیویورک، متعلق به کدام روز Daye، کدام سشن و کدام زیرسایکل است؟»

## داخل دامنه

- Broker timestamp adapter؛
- UTC instant؛
- New York wall clock؛
- US DST؛
- fold ساعت تکرارشده پاییز؛
- trading-day key از 18:00؛
- gap رسمی 17:00–18:00؛
- A/L/N/P؛
- a1 تا p4؛
- period windowهای محلی و UTC؛
- transition eventهای deterministic؛
- audit اختیاری.

## خارج از دامنه

- دریافت کندل دو نماد؛
- OHLC aggregation؛
- Hunt، SMT و confirmation؛
- رسم؛
- TWO/TDO؛
- سفارش، ریسک و معامله.

P01 هیچ وابستگی به EXP0017 و هیچ `CTrade` یا Order API ندارد.

