# EXP0017 Phase 01 — MQL5 Module Architecture

## هدف معماری

کد فاز ۱ باید کوچک، مستقل، قابل فهم و قابل توسعه باشد. اکسپرت اصلی نباید پر از جزئیات زمانی شود؛ جزئیات در ماژول‌ها جدا شده‌اند.

## فایل‌ها

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Time_Anatomy.mq5
mql5/Include/IntermarketDivergenceExecution/CG/CGT_Types.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGT_Time.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGT_Display.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGT_Engine.mqh
```

## نقش هر فایل

### `EXP0017_CG_Time_Anatomy.mq5`

نقطه ورود اکسپرت. فقط کارهای زیر را انجام می‌دهد:

- گرفتن inputها
- فعال‌کردن دو نماد پیش‌فرض
- ساخت تنظیمات زمان
- ساخت لیست CGهای فعال برای نمایش
- راه‌اندازی timer
- فراخوانی engine

### `CGT_Types.mqh`

قرارداد داده‌ها:

- شناسه CGها
- تعریف CG
- تنظیمات زمان
- snapshot زمان
- snapshot سایکل جاری

### `CGT_Time.mqh`

مغز زمانی فاز ۱:

- تبدیل broker time به UTC
- تبدیل UTC به New York
- تشخیص DST نیویورک
- ساخت روز معاملاتی 18:00 تا 17:00
- تشخیص داخل/خارج روز معاملاتی
- ساخت سایکل جاری هر CG
- تشخیص آخرین سایکل ناقص

### `CGT_Display.mqh`

زبان نمایش:

- ساخت panel چارت
- ساخت خط log اختیاری
- نمایش وضعیت CGها بدون ورود به منطق معامله

### `CGT_Engine.mqh`

هماهنگ‌کننده:

- رجیستری CGها
- فراخوانی Time Anatomy
- جمع‌کردن Cycle Snapshotها
- ارسال خروجی به Display

## چرا این جداسازی مهم است؟

چون فازهای بعدی باید روی همین لایه‌ها سوار شوند:

```text
Phase 02 Reference Anatomy -> نیازمند زمان و سایکل‌های قبلی
Phase 03 Hunt Anatomy -> نیازمند مرجع‌های زمانی
Phase 04 Divergence Anatomy -> نیازمند hunt و clean/hunter
Phase 05 Ledger -> نیازمند signal timestamps دقیق
```

اگر Time Anatomy داخل اکسپرت اصلی دفن شود، بعداً هر تغییر کوچک باعث خرابی کل پروژه می‌شود.

## مرز فاز ۱ در کد

کد فاز ۱ هیچ آبجکت تریدی ندارد، از `CTrade` استفاده نمی‌کند، دستور `Buy` یا `Sell` ندارد، هیچ SL/TP ندارد، و هیچ سیگنال واگرایی نمی‌سازد.
