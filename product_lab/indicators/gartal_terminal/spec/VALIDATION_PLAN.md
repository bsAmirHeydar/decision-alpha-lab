# Validation Plan — gartal terminal

## 1. هدف تست

قبل از فروش، این اندیکاتور باید از نظر زمان، داده، UI و alert سخت تست شود. محصول خبری اگر یک ساعت را اشتباه نشان دهد، اعتماد کاربر از بین می‌رود.

## 2. Test Matrix

| محور | سناریو | انتظار |
|---|---|---|
| Data | fetch موفق | eventها وارد dashboard شوند |
| Data | fetch fail | cache load شود |
| Data | cache missing | پیام خطای تمیز نمایش داده شود |
| Time | GMT broker دستی | زمان درست تبدیل شود |
| Time | auto GMT | اختلاف TimeCurrent/TimeGMT درست شود |
| UI | ۲۰ خبر در روز | dashboard خراب نشود |
| UI | ۵ خبر در یک ساعت | overlap کنترل شود |
| Alert | ۱۵ دقیقه قبل | فقط یک alert صادر شود |
| Alert | تغییر timeframe | alert دوباره تکرار نشود |
| Symbol | EURUSD | EUR/USD highlight شوند |
| Symbol | XAUUSD | USD/global risk highlight شود |

## 3. تست‌های روزهای خاص

- NFP Friday
- CPI day
- FOMC rate decision
- ECB press conference
- روز کم‌خبر
- Bank holiday
- روزی با چند speech

## 4. تست UI

- چارت dark
- چارت light
- مانیتور کوچک
- resolution بالا
- zoom in/out
- timeframeهای M1, M5, M15, H1, H4
- باز و بسته کردن dashboard

## 5. تست WebRequest

- URL whitelist نشده
- اینترنت قطع
- پاسخ HTML ناقص
- پاسخ خالی
- redirect
- timeout

## 6. تست Performance

- اجرای چند چارت همزمان
- ۱۰ اندیکاتور روی ۱۰ symbol
- refresh هر ۳۰ ثانیه نزدیک خبر
- تعداد object بالا

## 7. معیار قبولی نسخه فروش

- هیچ crash ندارد
- هر خطا در UI پیام دارد
- cache کار می‌کند
- alert duplicate نمی‌شود
- object leak ندارد
- uninstall/OnDeinit تمیز است
- user guide کامل است
