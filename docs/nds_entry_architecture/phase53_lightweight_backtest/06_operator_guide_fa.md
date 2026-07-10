# راهنمای اجرای بک‌تست سبک NDS

## فایل صحیح

در Strategy Tester این اکسپرت را انتخاب کن:

```text
NDSHookLimitF123Backtest.ex5
```

از اکسپرت سنگین `FlagCountingPhoenixExperiment` برای بک‌تست سریع استفاده نکن؛ آن فایل برای مشاهده، ممیزی و کل معماری production است.

## تنظیم پیشنهادی برای تست سریع

```text
InpBTProfile = FAST
InpBTTradeEnabled = true
InpBTSendTesterOrders = true
InpBTResetUsedSetupsOnInit = true
InpBTSkipHookRebuildWhilePositionOpen = true
InpBTPrintRunSummary = false
```

## تست تطبیقی نهایی

```text
InpBTProfile = PARITY
```

این حالت ۵۰۰۰ کندل و هشت scale اصلی را استفاده می‌کند و برای مقایسه با خروجی اکسپرت مرکزی مناسب است.

## نکات سرعت

- مدل تستر را متناسب با دقت موردنیاز انتخاب کن.
- برای منطق مبتنی بر closed bar، حالت `1 minute OHLC` معمولاً برای تست سریع مناسب‌تر است؛ اما قبل از پذیرش نهایی، همان سناریو را با ticks واقعی نیز کنترل کن.
- Visual mode را فقط برای نمونه‌های محدود روشن کن.
- CSV و printهای دوره‌ای در نسخه سبک به‌صورت پیش‌فرض خاموش‌اند.

## ایمنی

این فایل خارج از Strategy Tester با `INIT_FAILED` متوقف می‌شود. تنها با فعال‌کردن dry-run غیرتستر می‌توان آن را روی چارت اجرا کرد و در آن حالت ارسال سفارش اجباری خاموش می‌شود.
