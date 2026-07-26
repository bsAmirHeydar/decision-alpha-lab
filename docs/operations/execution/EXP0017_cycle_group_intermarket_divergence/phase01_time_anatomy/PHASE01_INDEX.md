# EXP0017 Phase 01 — CG Time Anatomy Index

فاز ۱ اولین لایه اجرایی EXP0017 است. هدف آن این نیست که واگرایی بگیرد یا معامله کند؛ هدف آن این است که ربات بتواند **زمان را مثل معمار استراتژی ببیند**.

## فایل‌های این فاز

- `PHASE01_TIME_ANATOMY_SPEC.md` — تعریف کامل فاز ۱
- `PHASE01_CYCLE_GROUP_CALENDAR_CONTRACT.md` — قرارداد تقویم CGها
- `PHASE01_MQL5_MODULE_ARCHITECTURE.md` — معماری ماژول‌های MQL5
- `PHASE01_VALIDATION_AND_TEST_PLAN.md` — برنامه تست و اعتبارسنجی
- `PHASE01_LIMITS_AND_NON_GOALS.md` — کارهایی که این فاز عمداً انجام نمی‌دهد
- `PHASE01_HANDOFF_TO_PHASE02.md` — تحویل فاز ۱ به فاز ۲

## کدهای اضافه‌شده

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Time_Anatomy.mq5
mql5/Include/IntermarketDivergenceExecution/CG/CGT_Types.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGT_Time.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGT_Display.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGT_Engine.mqh
```

## تعریف کوتاه

ربات در این فاز باید بتواند پاسخ دهد:

- الان در چه زمان بروکر هستیم؟
- معادل UTC چیست؟
- معادل نیویورک چیست؟
- آیا داخل روز معاملاتی 18:00 تا 17:00 نیویورک هستیم؟
- برای هر CG، سایکل جاری چیست؟
- برای هر CG، چند سایکل پیشین همان روز داریم؟
- آیا سایکل آخر روز ناقص است؟

## اصل مادر

> اگر زمان غلط باشد، مرجع غلط می‌شود؛ اگر مرجع غلط شود، هانت غلط می‌شود؛ اگر هانت غلط شود، واگرایی غلط می‌شود؛ اگر واگرایی غلط شود، آمار و مدل و AI هم آلوده می‌شوند.
