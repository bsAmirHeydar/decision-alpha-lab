---
id: EXP0018-P00-CONFLICT
title: "EXP0018 Phase 00 — Conflict Resolution Protocol"
type: standard
status: draft
project: EXP0018
version: 2.1.0
created: 2026-07-10
updated: 2026-07-10
owner: Strategy Architect
tags:
  - exp0018
  - daye-trader
  - phase00
  - doctrine-freeze
---

# پروتکل حل تعارض

## مراحل

1. تعارض با ID پایدار ثبت شود.
2. متن هر منبع بدون paraphrase گمراه‌کننده خلاصه شود.
3. مثال‌های مثبت و counterexample استخراج شود.
4. اثر هر گزینه بر Phaseها و schema مشخص شود.
5. recommendation مهندسی جدا از domain decision نوشته شود.
6. Strategy Architect گزینه را تصویب کند.
7. ADR از `proposed` به `accepted` تغییر کند.
8. decision ledger، rule registry، fixtures و downstream specs هم‌زمان به‌روزرسانی شوند.

## ممنوعیت‌ها

- انتخاب گزینه فقط چون «رایج‌تر» است؛
- استفاده از رفتار EXP0017 برای حل EXP0018؛
- مخفی‌کردن اختلاف Word و PDF؛
- پیاده‌سازی هر دو تفسیر زیر یک input بدون تصمیم صریح؛
- تبدیل uncertainty به default silent.

## تغییر بعد از Freeze

تغییر rule frozen فقط با ADR جدید، version bump، migration impact و replay comparison مجاز است.
