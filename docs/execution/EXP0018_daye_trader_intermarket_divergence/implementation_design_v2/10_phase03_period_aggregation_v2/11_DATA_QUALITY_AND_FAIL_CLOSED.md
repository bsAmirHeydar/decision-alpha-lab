---
id: EXP0018-P03-FAIL-CLOSED
title: "P03 Data Quality and Fail-Closed"
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

# کیفیت داده و Fail-Closed

موارد زیر period را invalid یا unavailable می‌کنند:

- base timeframe نامعتبر
- bar خارج از Window
- timestamp خارج از grid
- duplicate identity
- تعداد observed بیشتر از expected
- failure در time conversion
- نبود symbol history

Adapter failure اجازه تغییر حقیقت بازار را ندارد. P03 هرگز از نبود bar نتیجه clean/protected نمی‌گیرد.
