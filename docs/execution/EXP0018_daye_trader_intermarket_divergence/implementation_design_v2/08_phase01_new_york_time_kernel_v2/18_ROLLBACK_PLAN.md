---
id: EXP0018-P01-18-ROLLBACK-PLAN
title: "EXP0018 P01 — Rollback Plan"
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


# Rollback

این پچ فقط فایل‌های P01 را اضافه/جایگزین می‌کند. برای rollback:

1. commit این پچ را revert کن؛
2. EX5 جدید را حذف یا Expert قبلی را compile کن؛
3. فایل audit اختیاری را از Common Files پاک کن؛
4. هیچ migration داده یا state دائمی لازم نیست.

P01 هیچ تغییر schema در فازهای دیگر اعمال نمی‌کند.

