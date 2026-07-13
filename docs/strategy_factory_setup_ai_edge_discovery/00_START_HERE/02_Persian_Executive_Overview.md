---
id: SAED-B9390B503A
title: "نمای جامع فارسی سیستم AI Edge Discovery"
type: overview
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - persian
---

# نمای جامع فارسی سیستم AI Edge Discovery

## ایده‌ی مرکزی

این سیستم قرار نیست از روی قیمت خام هر چیزی اختراع کند. Context Engine قبلاً معنای بازار را به‌صورت دقیق، زمان‌مند و بدون نگاه به آینده تولید می‌کند. این ماژول روی هر رخداد معتبر Context می‌پرسد:

> آیا در این شرایط اصلاً معامله‌ای وجود دارد؟ اگر بله، کدام معماری سود و زیان، کدام روش ورود، کدام استاپ، کدام خروج و کدام مدیریت بیشترین Utility قابل دفاع را دارد؟

## پنج Payoff Profile اصلی

1. **Wide High-Hit Fixed** — استاپ ساختاری باز، هدف Win Rate بالا، Reward خالص حداقل 1R.
2. **Tight Convex Fixed** — استاپ تنگ، مقصد ثابت یا ساختاری، تمرکز بر Winnerهای چندR.
3. **Tight Convex Trail** — استاپ تنگ و خروج Trail؛ مسیر قیمت کاملاً مهم است.
4. **Wide Open Trail** — استاپ بزرگ، TP باز و دنبال‌کردن Trend تا پایان.
5. **Tight High-Hit Fixed** — استاپ تنگ، Reward حداقل 1R و هدف Timing بسیار دقیق با Win Rate بالا.

## سه Entry Mechanism اصلی

- Breakout/Stop Entry: خرید تأیید با قیمت بدتر و Slippage بیشتر.
- Immediate Market: خرید زمان و Fill قطعی‌تر، بدون Price Improvement.
- Pullback/Limit: خرید قیمت بهتر و هندسه بهتر استاپ، در ازای Non-Fill و Adverse Selection.

## کاری که AI انجام می‌دهد

AI چند کار جدا انجام می‌دهد:

- Trade/Skip/Review؛
- احتمال Trigger و Fill؛
- زمان تا Fill، Stop، Target یا Expiry؛
- توزیع MFE، MAE و Net R؛
- رتبه‌بندی Treatmentها؛
- انتخاب Treatment؛
- تشخیص Regime مناسب هر Style؛
- Uncertainty، Novelty و OOD؛
- انتخاب Fallback یا Abstention.

## چرا ضد Overfit است؟

- تمام Styleها، Entryها و Hyperparameterها قبل از Test نهایی Freeze می‌شوند.
- هر Context occurrence و همه‌ی Treatment siblingهایش در یک Cluster می‌مانند.
- Walk-forward، purge و embargo اجباری است.
- Manual baseline و Nullهای matched اجباری‌اند.
- Trialهای شکست‌خورده و حذف‌شده نیز در Multiplicity حساب می‌شوند.
- PBO، Deflated Performance، White/SPA، Parameter Stability، Cost/Delay Stress و Prospective Paper اجباری است.
- سود قوی نمی‌تواند Leakage، عدم Reproducibility یا Execution Failure را جبران کند.

## خروجی نهایی

خروجی صرفاً یک Model نیست؛ یک بسته کامل است:

```text
Frozen Context Package
+ Frozen Treatment Universe
+ Dataset/Fold Lineage
+ Model and Calibration
+ Manual Baseline Comparison
+ Statistical Evidence
+ Null and Stress Results
+ Policy Graph
+ Abstention/Fallback
+ Runtime Parity Vectors
+ Monitoring Assumptions
```

تا زمانی که این بسته از Gateهای I12 تا I18 عبور نکرده باشد، Model هیچ اجازه‌ی اجرای معامله ندارد.
