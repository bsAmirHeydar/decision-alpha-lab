# راهنمای نصب مشتری — gartal terminal

## فایل‌های پکیج

پکیج مشتری معمولاً شامل این‌هاست:

```text
MQL5/Indicators/GartalTerminal/GartalTerminal.ex5
MQL5/Experts/GartalTerminal/GartalNewsDownloaderEA.ex5
MQL5/Presets/gartal_terminal_live_bridge.set
MQL5/Presets/gartal_terminal_stable_customer.set
docs/
fixtures/
```

## نصب

1. متاتریدر ۵ را باز کن.
2. از مسیر `File > Open Data Folder` وارد دیتافولدر شو.
3. فایل `GartalTerminal.ex5` را داخل `MQL5/Indicators/GartalTerminal/` کپی کن.
4. فایل `GartalNewsDownloaderEA.ex5` را داخل `MQL5/Experts/GartalTerminal/` کپی کن.
5. فایل‌های `.set` را داخل `MQL5/Presets/` کپی کن.
6. متاتریدر را ری‌استارت کن یا Navigator را Refresh کن.

## اجازه WebRequest

برای اینکه EA دانلودر بتواند خبرها را بگیرد، این آدرس باید در MT5 مجاز شود:

```text
Tools > Options > Expert Advisors > Allow WebRequest for listed URL
https://nfs.faireconomy.media
```

خود اندیکاتور از فایل local bridge می‌خواند:

```text
MQL5/Files/GartalTerminal/ff_calendar_thisweek.xml
```

## تنظیم پیشنهادی

1. EA دانلودر را روی یک چارت جدا اجرا کن.
2. اندیکاتور `GartalTerminal` را روی چارت‌های معاملاتی بینداز.
3. برای نسخه بتا، preset `gartal_terminal_live_bridge.set` را لود کن.
4. اول حالت GMT auto/hybrid را تست کن.
5. اگر زمان بروکر خاص بود، offset دستی را تنظیم کن.

## هشدار محصول

`gartal terminal` ابزار نمایش و هشدار اخبار ماکرو است. نتیجه خبر را پیش‌بینی نمی‌کند و در زمان انتشار خبر، تضمین اجرای امن معامله نمی‌دهد.
