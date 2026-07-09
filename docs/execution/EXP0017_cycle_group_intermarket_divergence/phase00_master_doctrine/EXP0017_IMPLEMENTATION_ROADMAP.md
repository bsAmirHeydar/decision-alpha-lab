# EXP0017 — Implementation Roadmap After Phase 00

## فلسفه پیاده‌سازی

پیاده‌سازی نباید از معامله شروع شود. ابتدا ربات باید مثل معمار استراتژی ببیند. بعد ثبت کند. بعد آمار بگیرد. بعد مدل شود. بعد تصمیم ساخته شود. اجرا آخرین لایه است.

## Level 01 — Time Anatomy

هدف: فهم روز معاملاتی و سایکل‌گروپ‌ها.

خروجی:

- تشخیص روز معاملاتی 18:00 تا 17:00 نیویورک
- تشخیص CGهای فعال
- تشخیص سایکل جاری هر CG
- تشخیص سایکل‌های قبلی همان روز
- نمایش وضعیت روی چارت یا گزارش

بدون واگرایی. بدون ترید.

## Level 02 — Symbol Pair Anatomy

هدف: فهم رابطه دو نماد بدون مقایسه قیمت خام.

خروجی:

- SPXUSD نسبت به مرجع خودش
- NDXUSD نسبت به مرجع خودش
- هم‌زمانی رفتاری
- آمادگی برای ساخت مرجع‌ها

## Level 03 — Reference Field Anatomy

هدف: ساخت میدان مرجع برای high/low سایکل‌های قبلی همان روز.

خروجی:

- reference high/low برای هر نماد
- reference cycle identity
- reference distance
- fresh/hunted/invalidated state

## Level 04 — Hunt Anatomy

هدف: تشخیص touch/break/equal high/equal low.

خروجی:

- hunt events
- hunter symbol
- hunt side
- hunt time
- hunt candle
- reference consumed/active state

## Level 05 — Divergence Anatomy

هدف: ساخت واگرایی از اختلاف هانت دو نماد.

خروجی:

- potential divergence
- direction
- hunter symbol
- clean symbol
- reference pair

## Level 06 — Confirmation and Invalidation Anatomy

هدف: تبدیل واگرایی بالقوه به تاییدشده و ثبت ابطال.

خروجی:

- confirmed signal
- trade permission
- invalidation before confirmation
- invalidation after confirmation
- double-hunt logic

## Level 07 — Visual Language

هدف: نشان دادن دید ربات روی چارت.

خروجی:

- خطوط هانت
- لیبل CG
- جهت
- hunter/clean
- reference cycle
- confirmation candle

## Level 08 — Signal Ledger

هدف: ثبت تمام سیگنال‌های تاییدشده و قابل معامله.

خروجی:

- CSV/JSON signal ledger
- raw research memory
- بدون تصمیم و بدون فیلتر آماری

## Level 09 — Outcome Study

هدف: سنجش نتیجه هر سیگنال.

خروجی:

- cycle-end outcome
- post-cycle windows
- max intraday reward
- stop result
- dollar/R/pip/normalized pip

## Level 10 — Statistical Reports

هدف: شناخت خانواده‌ها.

خروجی:

- گزارش CG
- گزارش زمان
- گزارش جهت
- گزارش نماد سالم/هانتر
- گزارش overlap
- گزارش stop streak

## Level 11 — Model-Ready Dataset

هدف: آماده‌سازی داده برای مدل آماری و AI.

خروجی:

- dataset تمیز
- field catalog کامل
- labeling قابل تکرار

## Level 12 — Ranking and Comparison Model

هدف: تحلیلگر، رتبه‌دهنده، مقایسه‌گر.

خروجی:

- quality score
- family ranking
- risk warning
- statistical comparison

## Level 13 — Decision Gate

هدف: معمار استراتژی براساس آمار تصمیم می‌گیرد چه چیزی وارد نسخه اجرایی شود.

## Level 14 — Raw Execution

اجرای همه سیگنال‌های معتبر خام، اگر لازم باشد.

## Level 15 — Filtered Execution

فقط بعد از آمار و تصویب، قوانین منتخب اجرا می‌شوند.

## Level 16 — AI Analyst Layer

AI گزارش‌ها را می‌خواند، خانواده‌ها را مقایسه می‌کند، و پیشنهادهای غیرخودکار می‌دهد.

## اصل مسیر

```text
Anatomy → Observation → Ledger → Statistics → Model → Decision → Execution
```
