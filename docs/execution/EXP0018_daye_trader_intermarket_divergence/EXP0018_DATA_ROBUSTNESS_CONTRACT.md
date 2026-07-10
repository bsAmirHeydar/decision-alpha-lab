# قرارداد پایداری داده و چارت

## اصول

- محاسبات با timestamp انجام شوند، نه bar count ثابت.
- missing bar نباید باعث array out of range شود.
- تاریخچه هر دو نماد باید مستقل validate شود.
- signal فقط وقتی ساخته شود که هر دو نماد برای current و reference داده معتبر داشته باشند.

## Expiry / Roll

اگر نماد تاریخچه کوتاه دارد:

- برنامه crash نکند.
- به قدیمی‌ترین period کامل قابل‌دسترسی محدود شود.
- period ناقص نباید به‌جای period کامل silently استفاده شود.

## Weekend

- شنبه و یکشنبه period معاملاتی جدید تولید نکنند.
- عبور PA و p4→a1 باید trading-day aware باشد.

## تفاوت bar count

وجود bar کمتر یا بیشتر در روز نباید time windowها را تغییر دهد.

## خطاهای قابل گزارش

- symbol unavailable
- history unavailable
- partial reference
- partial current period
- timezone conversion failure
- object creation failure
