---
id: EXP0018-P03-ROLLBACK
title: "P03 Rollback Plan"
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

# Rollback

Rollback فقط فایل‌های P03 را حذف یا به commit قبل برمی‌گرداند. P01 و P02 نباید rollback شوند. CSVهای تولیدشده P03 evidence مشتق‌شده‌اند و پس از rollback می‌توانند پاک شوند. هیچ migration روی strategy state یا حساب معاملاتی وجود ندارد.
