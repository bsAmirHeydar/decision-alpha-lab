---
id: EXP0018-P03-PAIRED-STORE
title: "P03 Paired Period Store"
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

# Paired Period Store

Paired Period مقیاس‌های قیمت را ترکیب نمی‌کند؛ فقط دو Snapshot هم‌هویت را زیر یک Window مشترک نگه می‌دارد. اگر یک نماد period را ندارد، placeholder با `UNAVAILABLE` ساخته می‌شود. aligned count از exact pairهای P02 در همان Window شمارش می‌شود.

Paired Period زمانی `COMPLETE` است که هر دو symbol period کامل باشند و تعداد exact aligned bar برابر expected باشد. وجود OHLC کافی نیست؛ هم‌ترازی زمانی نیز باید کامل باشد.
