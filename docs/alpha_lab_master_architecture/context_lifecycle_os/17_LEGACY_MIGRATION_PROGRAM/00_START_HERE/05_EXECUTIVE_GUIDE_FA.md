---
title: "راهنمای اجرایی فارسی برنامه مهاجرت LCM"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, fa]
---
# راهنمای اجرایی فارسی برنامه مهاجرت LCM

این برنامه برای انتقال منطق‌های قبلی به ACL-OS طراحی شده است، اما انتقال را با جابه‌جایی فایل شروع نمی‌کند. ابتدا باید دقیقاً بدانیم هر فایل چه نقشی دارد، مالک معنای آن چه کسی است، رفتار فعلی آن چیست و اگر تغییر کند کدام خروجی‌ها می‌شکنند.

## قاعده اصلی

هر منطق قدیمی باید دو هویت هم‌زمان داشته باشد:

- هویت مشاهده‌شده Legacy؛
- هویت Canonical مورد تأیید مالک.

اگر رفتار فعلی با منظور واقعی مالک فرق دارد، مهاجرت ابتدا رفتار فعلی را ثبت می‌کند و سپس اصلاح را در نسخه جدید و در یک کامیت مستقل انجام می‌دهد. این تفکیک مانع می‌شود Bug Fix داخل Refactor پنهان شود.

## ترتیب غیرقابل تغییر

۱. Freeze کامل وضعیت فعلی؛ ۲. Inventory ماشینی؛ ۳. تعیین مالک و کلاس هر فایل؛ ۴. ثبت رفتار و Event Trace؛ ۵. ساخت Spec استاندارد؛ ۶. Adapter؛ ۷. مقایسه Legacy و Canonical؛ ۸. Dual Run؛ ۹. Cutover؛ ۱۰. Quarantine؛ ۱۱. حذف کنترل‌شده.

## تصمیم معماری برای پروژه فعلی

- ACL-OS و Strategy Factory مقصد مهاجرت هستند، نه Context قدیمی.
- Contextهای واقعی باید زیر `lab/11_strategy_factory/contexts/<context_id>` قرار گیرند.
- Setupها، Treatmentها و Visualizerها باید کتابخانه مستقل داشته باشند و دوباره داخل Expertهای یکپارچه مخلوط نشوند.
- MQL5 Canonical باید در Namespace واحد `AlphaLab/ContextOS` ساخته شود؛ مسیرهای قدیمی تا پایان Dual Run با Wrapper نگه داشته می‌شوند.
- اسناد Canonical باید زیر Master Architecture یا داخل Context Package باشند. Obsidian projectionهای مشتق‌شده منبع حقیقت نیستند.
- فایل‌های Release، Hash، Manifest و Commit Message نباید در Root باقی بمانند؛ ولی انتقال آن‌ها نیز مرحله‌ای و با Locator انجام می‌شود.

## ترتیب موج‌های مهاجرت

موج اول باید منطق‌های Read-Only و کم‌ریسک باشد. منطق‌های MTF، Session، Drawing و Stateful بعد از آن می‌آیند. Faerie Protocol، EXP0017، FlagCounting/NDS/Hook و تمام Execution Adapterها در موج‌های دیرتر قرار می‌گیرند.

## تعریف پایان واقعی

یک Context زمانی مهاجرت‌شده است که Spec، Known-Time، State Machine، Golden Trace، Parity، Documentation، ACL-OS Binding، Rollback و Quarantine کامل داشته باشد. صرف Compile شدن یا منتقل‌شدن فایل به پوشه جدید مهاجرت محسوب نمی‌شود.
