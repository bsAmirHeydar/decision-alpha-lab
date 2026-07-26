---
id: EXP0018-P03-RUNTIME
title: "P03 Runtime Validation Guide"
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

# راهنمای بررسی Runtime

1. هر دو نماد را در Market Watch فعال کن.
2. History M1 را کامل کن.
3. Expert را روی یک چارت attach کن.
4. در Experts باید embedded tests برابر PASS باشد.
5. Summary باید حداقل چند complete period داشته باشد.
6. جدیدترین period معمولاً OPEN و period قبلی COMPLETE یا PARTIAL است.
7. در روز DST countهای Daily را با duration UTC بررسی کن.
8. Audit CSV را فقط برای بررسی محدود روشن کن.

این Expert چیزی روی چارت رسم نمی‌کند.
