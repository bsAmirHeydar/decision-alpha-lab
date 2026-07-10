# مدل یکپارچه True Open

## تعریف مشترک

True Open معمولاً open اولین candle در Q2 هر cycle است. نقش‌های ذکرشده:

- مرز premium/discount زمانی؛
- فیلتر جهت SMT؛
- حمایت/مقاومت پویا؛
- anchor برای breaker یا precision level؛
- سنجش stacked context میان cycleها.

## زمان‌های تکرارشونده در منابع

- True Year Open: اولین دوشنبه آوریل / شروع Q2 سالانه
- True Month Open: شروع هفته کامل دوم ماه
- True Week Open: Tuesday open که در ساعت 18:00 دوشنبه نیویورک شروع می‌شود
- True Day Open: 00:00 نیویورک
- True Session Open: 19:30، 01:30، 07:30، 13:30
- True Micro Session Open: 22.5 دقیقه بعد از شروع micro cycle

## رابطه با Word اصلی

Word فقط TWO و TDO را به‌عنوان رسم رسمی درخواست کرده است. سایر True Openها enrichment هستند و باید در ماژول جدا، با input مستقل و بدون تغییر detector اصلی ساخته شوند.

## ابهام حیاتی

عبارت «سه‌شنبه ۱۸:۰۰» در Word باید با «Tuesday open / Monday 18:00 NY» از PDFها دقیقاً reconcile شود. تا تصمیم معمار، تعریف موجود در قرارداد اصلی حفظ می‌شود.
