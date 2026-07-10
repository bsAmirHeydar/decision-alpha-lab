---
id: EXP0018-P03-IO
title: "P03 Input Output and Schema"
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

# ورودی و خروجی

ورودی‌های کلیدی شامل symbol mapping، base timeframe، lookback bars، خانواده‌های فعال، سیاست انتشار partial/open و time adapter است. Audit CSV اختیاری است و recordهای `SUMMARY/EVENT/PERIOD` دارد.

خروجی Snapshot همیشه `schema_version`، stable ID، UTC/NY Window، OHLC symbol-local، expected/observed counts، completeness، reason code و previous links دارد.
