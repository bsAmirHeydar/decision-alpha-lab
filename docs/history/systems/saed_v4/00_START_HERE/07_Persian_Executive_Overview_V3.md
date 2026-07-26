---
title: Persian Executive Overview V3
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v4
  - persian
  - executive
---

# نمای اجرایی فارسی

این معماری برای ساخت یک مدل واحد نیست. هدف، ساخت یک **کارخانه نهادی کشف اج** است که بتواند صدها Context را به‌صورت مستقل و عمیق یاد بگیرد، اما همه آن‌ها را روی یک زیرساخت مشترک، قابل بازسازی و تحت حاکمیت UCEE اداره کند.

## اصل اول: هر Context یک Cell مستقل

هر Cell شامل حقیقت Context، آنتولوژی، Support Geometry، Treatment Lattice، Outcome Cube، مدل‌ها، Red Team، Evidence Ledger، Policy و Monitoring است. افزودن Context جدید نباید باعث Fork شدن Engine مرکزی شود.

## اصل دوم: AI اکشن آزاد اختراع نمی‌کند

AI فقط بین Treatmentهای معتبر و از قبل Compile‌شده انتخاب می‌کند. `Skip` و `Abstain` اکشن رسمی‌اند. AI حق تعیین ریسک نهایی، حجم، سفارش، تغییر Context، Promotion یا فعال‌سازی Runtime ندارد.

## اصل سوم: بهترین Backtest معیار برنده‌شدن نیست

معیار اصلی، کران پایین Utility خالص پس از Cost، Tail، Capacity، Capital Occupancy، Multiplicity، Drift، Feed/Broker Transport، حذف بهترین معاملات، Hidden Evaluation و Prospective Paper است.

## اصل چهارم: تمام جست‌وجو بخشی از آزمون آماری است

هر Trial، Retry، Prune، نمودار دیده‌شده، خروجی Agent، تغییر Narrative و Query به Hidden Test در Exposure Ledger ثبت می‌شود. سیستم از Online FDR و Query Budget استفاده می‌کند تا خود فرایند تحقیق به منبع اج کاذب تبدیل نشود.

## اصل پنجم: پیشرفته‌ترین AI فقط Challenger است

Foundation Model، Transformer، State-Space، Graph Network، Causal Learner، World Model و Offline RL می‌توانند تحقیق را عمیق‌تر کنند؛ اما هیچ‌کدام بدون برتری واقعی نسبت به Manual و Baseline ساده، آزمون مستقل، Prospective Evidence و Runtime Parity اجازه ورود ندارند.

## نتیجه

SAED V4 باید بتواند برای هر Context پاسخ دهد:

```text
در این Occurrence مشخص،
در کدام Support و Regime،
کدام Payoff Profile، Entry Mechanism و Treatment کامل،
با چه احتمال Fill، Distribution، Tail، Cost، Capacity و Uncertainty،
نسبت به Skip و Manual Policy ارزش افزوده قابل دفاع دارد؟
```

اگر پاسخ قابل دفاع نباشد، خروجی صحیح معامله نیست؛ `Skip`، `Abstain`، `Manual Fallback` یا `Reject` است.
