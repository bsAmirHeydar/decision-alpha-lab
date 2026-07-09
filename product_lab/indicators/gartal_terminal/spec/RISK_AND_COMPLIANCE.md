# Risk and Compliance Notes

## 1. Data Rights

برای نسخه فروش باید وضعیت مجوز استفاده از منبع داده مشخص شود. اگر داده مستقیم از یک وب‌سایت عمومی خوانده می‌شود، ممکن است تغییر ساختار، محدودیت دسترسی، یا محدودیت استفاده تجاری وجود داشته باشد.

راه امن‌تر برای محصول پولی:

- ساخت API bridge اختصاصی
- cache سمت سرور
- rate limit
- امکان تغییر source بدون تغییر indicator
- بررسی حقوقی/تجاری قبل از فروش بزرگ

## 2. Trading Disclaimer

محصول نباید وعده سود بدهد. متن پیشنهادی:

```text
Gartal terminal is a market information and risk-awareness tool. It does not provide financial advice, trade signals, or guaranteed outcomes.
```

## 3. Reliability Disclaimer

خبرها ممکن است با تأخیر، خطای منبع، تغییر زمان یا اصلاح داده همراه باشند. UI باید source status و last refresh را نمایش دهد.

## 4. Paid Product Risk

برای فروش اشتراکی باید این موارد آماده شود:

- user agreement
- refund policy
- license terms
- data-source disclaimer
- support scope
- update policy

## 5. Technical Risk

- Forex Factory HTML ممکن است تغییر کند
- WebRequest ممکن است در سیستم کاربر whitelist نشده باشد
- بروکرها ساعت متفاوت دارند
- DST باعث اختلاف زمانی می‌شود
- بعضی خبرها actual/forecast/previous ندارند

راهکار: معماری adapter + cache + status dashboard.
