---
title: "EXP0013 — Astro Path Cleanliness Screen Guide"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "13219"
entities:
  - "EXP0013"
concepts:
  - "Astro ML"
  - "Execution"
  - "MQL Native"
---


# EXP0013 — Astro Path Cleanliness Screen Guide

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `13219` bytes

## خلاصه

این دمو هیچ معامله‌ای باز نمی‌کند. هدفش فقط این است که در Visual Tester یا اجرای live، روی هر کندل ببینیم وضعیت آسمان از نظر **تمیزی مسیر** چه شکلی است. ما در این فاز دنبال جهت نیستیم. سؤال این نیست که آسترولوژی Buy می‌دهد یا Sell. سؤال این است: پس این Expert فقط یک ابزار مشاهده و کالیبراسیون است. فایل CSV باید قبلاً با Python ساخته شده باشد و داخل این مسیر در ترمینال متاتریدر قرار بگیرد: مثلاً: روی چارت یا Visual Tester این Expert را اجرا کن: inputهای مهم: قانون زمان: اگر ساعت بروکر UTC+2 است، offset باید `2.0` باشد. اگر UTC+3 است، باید `3.0` باشد. اگر این عدد غلط باشد، نقشه آسمان به کندل اشتباه وصل می‌شود و کل تحقیق خراب می‌شود. این ماژول وضعیت خام آسترولوژی را به چند محور قابل تست تبدیل م

## Headings

- EXP0013 — Astro Path Cleanliness Screen Guide
-   هدف این صفحه
-   فایل‌های مربوط
-   اجرای دمو
- فلسفه‌ی متریک‌ها
-   1. Flow
-   2. Impulse
-   3. Friction
-   4. Pressure
-   5. Transition
-   6. MoonTempo
-   7. SaturnDrag

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_COMMON_FILES_TESTER_FIX|EXP0013 Astro CSV — Strategy Tester Common Files Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_DIAGNOSTIC_GUIDE|EXP0013 Astro CSV Runtime Diagnostic Guide]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_FILES_ROOT_FALLBACK|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_CSV_RUNTIME_PATH_AND_PANEL_FIX|EXP0013 Astro CSV Runtime Path and Panel Diagnostics]] — `experiment`
- [[docs/evidence/exp0013_astro_csv_runtime_path_fix/ad8f4c6e752a_ASTRO_CSV_RUNTIME_PATH_FIX|EXP0013 Astro CSV Runtime Path Fix]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|EXP0013 Astro Dashboard V2 - Cockpit Layout]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|EXP0013 Astro Dashboard V3 - Interactive Cockpit]] — `experiment`
- [[docs/evidence/astro_doctrine/f9353abb5fd5_ASTRO_DOCTRINE_V1|ASTRO Doctrine V1]] — `experiment`
- [[docs/evidence/exp0013_astro_fractal_m1_oscillator_guide/497686de5688_ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|EXP0013 Astro Fractal M1 Oscillator Guide]] — `experiment`
- [[docs/evidence/exp0013_astro_time_contract_no_second_gmt_shift/dff6c2da3787_ASTRO_NO_SECOND_GMT_SHIFT|EXP0013 Astro Time Contract: No Second GMT Shift]] — `experiment`
- [[docs/evidence/exp0013_astro_only_execution_contract/b50b0013f3c9_ASTRO_ONLY_EXECUTION_CONTRACT|EXP0013 Astro-Only Execution Contract]] — `experiment`
- [[docs/evidence/exp0013_astro_only_execution_roadmap/d577cd434dcb_ASTRO_ONLY_EXECUTION_ROADMAP|EXP0013 Astro-Only Execution Roadmap]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
