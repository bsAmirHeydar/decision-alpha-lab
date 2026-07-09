# gartal terminal

`gartal terminal` یک اندیکاتور خبری/ماکرو برای چارت است که تقویم اقتصادی روز را به شکل قابل معامله روی چارت تبدیل می‌کند: داشبورد مرکزی، تایم‌لاین خبرهای آینده، رنگ‌بندی impact، فیلتر داخلی، هشدار چندمرحله‌ای، و معماری ماژولار برای دریافت خبر از Forex Factory یا هر منبع جایگزین.

> هدف این پوشه ساخت محصول قابل فروش است، نه فقط یک اسکریپت آزمایشی.

## تعریف کوتاه محصول

- **نام محصول:** gartal terminal
- **نوع:** MT5 Indicator / Macro News Terminal
- **ورژن پایه:** `v0.1.0-product-architecture`
- **بازار اولیه:** تریدرهای فارکس، طلا، شاخص‌ها و پراپ
- **منطق اصلی:** تبدیل Calendar به سطح زمانی قابل دیدن روی چارت
- **داده پیش‌فرض:** اخبار امروز
- **نمایش پیش‌فرض:** داشبورد + خط زمانی پایین چارت + خط عمودی روی لحظه خبر
- **مدل زمانی:** UTC source → Broker time display با auto/override offset

## خروجی‌های اصلی

1. **Dashboard**
   - ساعت خبر
   - ارز مرتبط
   - رنگ خبر/impact
   - عنوان خبر
   - actual / forecast / previous
   - وضعیت: upcoming / live / released / revised
   - زمان باقی‌مانده

2. **Chart Timeline**
   - خط یا marker خبرهای باقی‌مانده روز در پایین چارت
   - قرارگیری در زمان واقعی خبر روی محور زمانی چارت
   - نمایش جلوتر از قیمت فعلی تا انتهای روز، در صورت وجود کندل آینده/shift یا روش object projection

3. **Vertical Event Lines**
   - خط عمودی در timestamp خبر
   - رنگ بر اساس impact
   - label کوتاه کنار خط
   - حالت compact/full

4. **Filter Panel**
   - فیلتر ارزها
   - فیلتر impact
   - فیلتر بازه زمانی
   - فیلتر speech / holiday / tentative / breaking
   - فیلتر chart-symbol auto detect

5. **Alert Engine**
   - قبل از خبر: 60/30/15/5/1 دقیقه
   - لحظه خبر
   - بعد از انتشار actual
   - فقط High impact
   - فقط ارزهای چارت
   - popup / sound / push / email

## مسیرهای مهم

```text
product_lab/indicators/gartal_terminal/
├── README.md
├── 00_OBSIDIAN_START_HERE.md
├── mql5/
│   ├── GartalTerminal.mq5
│   └── include/
├── obsidian/
├── release/
├── screenshots/
├── scripts/
└── spec/
```

## وضعیت این پچ

این پچ مرحله اول محصول را می‌سازد:

- داکیومنت محصولی کامل
- معماری ماژولار
- اسکلت MQL5
- طراحی UI/UX
- مدل داده
- مدل alert
- مدل parser
- مدل انتشار و فروش

این نسخه هنوز «نسخه نهایی قابل فروش» نیست. مرحله بعدی باید اتصال داده، parser واقعی، تست روی MT5، و hardening انجام شود.
