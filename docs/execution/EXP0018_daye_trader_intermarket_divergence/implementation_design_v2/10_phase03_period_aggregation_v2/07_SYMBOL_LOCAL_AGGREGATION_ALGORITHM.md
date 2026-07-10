---
id: EXP0018-P03-ALGORITHM
title: "P03 Symbol-Local Aggregation Algorithm"
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

# الگوریتم تجمیع symbol-local

برای هر bar به‌ترتیب زمانی:

1. UTC bar به New York wall time تبدیل می‌شود.
2. اگر bar در Gap باشد کنار گذاشته می‌شود.
3. Windowهای Daily، Session و Subcycle resolve می‌شوند.
4. Snapshot مربوط به `period_instance_id` پیدا یا ساخته می‌شود.
5. Open فقط از اولین bar، Close فقط از آخرین bar و High/Low از extrema همان نماد ساخته می‌شود.
6. Volume و Spread تجمیع می‌شوند.
7. بعد از پایان scan، expected grid و completeness محاسبه می‌شود.

هیچ قیمت نماد B در OHLC نماد A وارد نمی‌شود.
