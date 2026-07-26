---
id: EXP0018-P03-PERFORMANCE
title: "P03 Performance and Determinism"
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

# کارایی و Determinism

Refresh فقط با تغییر latest closed bar یا force interval انجام می‌شود. Scan تاریخی bounded است. Aggregation symbol-local یک‌بار روی barها انجام می‌شود. Period store حداکثر با input محدود می‌شود.

ورودی یکسان، time config یکسان و history یکسان باید ID، OHLC، completeness و previous links یکسان تولید کنند.
