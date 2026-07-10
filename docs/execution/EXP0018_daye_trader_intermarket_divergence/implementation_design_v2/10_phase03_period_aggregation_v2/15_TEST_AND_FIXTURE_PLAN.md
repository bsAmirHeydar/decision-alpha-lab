---
id: EXP0018-P03-TESTS
title: "P03 Test and Fixture Plan"
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

# برنامه تست

سناریوهای اجباری:

- p4 کامل با دقیقاً ۳۰ bar M1
- p4 بسته و ناقص
- period باز
- period بدون داده
- Session P پنج‌ساعته
- Daily معمولی، Spring DST و Fall DST
- lookback که از وسط Session شروع می‌شود
- bar خارج از grid
- یک symbol کامل و دیگری unavailable
- previous chronological برای p4→a1
- اجرای دوباره و ID یکسان

تست Python مستقل از MQL5 منطق count/completeness را کنترل می‌کند؛ MetaEditor compile همچنان gate جداست.
