
---
type: source_card
source_path: "lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE.md"
source_ext: ".md"
source_size: 13219
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Convexity / Optionality", "Execution / Risk", "MQL Native", "Path Smoothness", "Python Brain", "UI / React"]
entities: ["EXP0013"]
---

# Source Card — ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE.md

## Source

[[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE|lab/03_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE.md]]

## Summary

این دمو هیچ معامله‌ای باز نمی‌کند. هدفش فقط این است که در Visual Tester یا اجرای live، روی هر کندل ببینیم وضعیت آسمان از نظر **تمیزی مسیر** چه شکلی است. ما در این فاز دنبال جهت نیستیم. سؤال این نیست که آسترولوژی Buy می‌دهد یا Sell. سؤال این است: پس این Expert فقط یک ابزار مشاهده و کالیبراسیون است. فایل CSV باید قبلاً با Python ساخته شده باشد و داخل این مسیر در ترمینال متاتریدر قرار بگیرد: مثلاً: روی چارت یا Visual Tester این Expert را اجرا کن: inputهای مهم: قانون زمان: اگر ساعت بروکر UTC+2 است، offset باید `2.0` باشد. اگر UTC+3 است، باید `3.0` باشد. اگر این عدد غلط باشد، نقشه آسمان به کندل اشتباه وصل می‌شود و کل تحقیق خراب می‌شود. این ماژول وضعیت خام آسترولوژی را به چند محور قابل تست تبدیل می‌کند: همه امتیازها از 0 تا 100 هستند. عدد بالا همیشه خوب نیست. معنی هر محور فرق دارد. `Flow` یعنی روانی هندسه آسمان. در پروژه ما این را این‌طور می‌خوانیم: Flow بیشتر از aspectهای نرم ساخته می‌شود: جف

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0013

## Headings

- EXP0013 — Astro Path Cleanliness Screen Guide
  - هدف این صفحه
  - فایل‌های مربوط
  - اجرای دمو
- فلسفه‌ی متریک‌ها
  - 1. Flow
  - 2. Impulse
  - 3. Friction
  - 4. Pressure
  - 5. Transition
  - 6. MoonTempo
  - 7. SaturnDrag

## Related Source Documents

- [[lab/03_experiments/EXP0013_astro_feature_store/RUN_ASTRO_RAW_AXES_OSCILLATOR|RUN_ASTRO_RAW_AXES_OSCILLATOR.md]] — score `20`
- [[mql5/Experts/AstroExecution/README|README.md]] — score `19`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V2_COCKPIT_GUIDE|ASTRO_DASHBOARD_V2_COCKPIT_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE|ASTRO_DASHBOARD_V3_INTERACTIVE_COCKPIT_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE|ASTRO_FRACTAL_M1_OSCILLATOR_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_NO_SECOND_GMT_SHIFT|ASTRO_NO_SECOND_GMT_SHIFT.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_ONLY_EXECUTION_CONTRACT|ASTRO_ONLY_EXECUTION_CONTRACT.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_RAW_AXES_OSCILLATOR_GUIDE|ASTRO_RAW_AXES_OSCILLATOR_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/ASTRO_UNIFIED_DASHBOARD_EA_GUIDE|ASTRO_UNIFIED_DASHBOARD_EA_GUIDE.md]] — score `18`
- [[lab/03_experiments/EXP0013_astro_feature_store/BUILD_EXCEL_COMMANDS|BUILD_EXCEL_COMMANDS.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
