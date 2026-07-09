# Data Source and Parser Model

## 1. هدف لایه داده

لایه داده باید خبرها را از منبع خام بگیرد و به یک ساختار داخلی ثابت تبدیل کند. UI نباید بداند داده از Forex Factory آمده، API آمده یا فایل cache.

## 2. معماری پیشنهادی

```text
ForexFactory HTML / API / Cache
        │
        ▼
Calendar Client
        │ raw text/html/json
        ▼
Parser Adapter
        │ normalized events
        ▼
News Store + Cache
        │ filtered events
        ▼
Dashboard / Timeline / Alerts
```

## 3. منابع داده

### Source A — Forex Factory Direct

- مناسب برای نسخه اولیه و تست
- نیازمند MT5 WebRequest whitelist
- ریسک: تغییر ساختار HTML
- نیازمند parser مقاوم

### Source B — API Bridge

- مناسب نسخه فروش پایدارتر
- می‌تواند روی سرور خودمان باشد
- خروجی JSON تمیز می‌دهد
- امکان caching و license-control دارد

### Source C — Local Cache

- برای زمانی که اینترنت قطع است
- آخرین خبرهای موفق را نگه می‌دارد
- UI را fail-safe می‌کند

## 4. ساختار Event داخلی

```text
EventId
Source
SourceUrl
DateUtc
TimeUtc
TimeBroker
Currency
Impact
EventType
Title
Actual
Forecast
Previous
Status
IsTentative
IsSpeech
IsHoliday
IsBreaking
IsRelevantToCurrentSymbol
AlertState
RawRowHash
LastUpdatedUtc
```

## 5. Impact Mapping

```text
ForexFactory Red       → HIGH
ForexFactory Orange    → MEDIUM
ForexFactory Yellow    → LOW
Gray / Bank Holiday    → HOLIDAY
Speech / Speaker       → SPEECH flag
Tentative              → TENTATIVE flag
Unexpected Red Headline → BREAKING flag when source supports it
```

## 6. خبرهای ناگهانی و سخنرانی‌ها

در Forex Factory بعضی speechها یا eventهای سیاسی/بانکی ممکن است با impact بالا بیایند. محصول باید:

- title شامل `Speaks`, `Speech`, `Testifies`, `Press Conference`, `Statement`, `Chair`, `President`, `Treasury`, `FOMC`, `ECB` را speech-class کند
- اگر impact قرمز بود، حتی اگر event تقویمی نبود، در داشبورد high-risk نشان دهد
- برای موارد غیرتقویمی واقعی، نسخه بعدی باید news feed adapter جدا داشته باشد

## 7. Breaking News Strategy

نسخه اول:

- هر event قرمز/High که title آن speech/political/risk باشد، در UI به عنوان high alert نشان داده می‌شود
- اگر source فقط calendar بدهد، breaking خارج از calendar تضمین نمی‌شود

نسخه حرفه‌ای:

- یک `BreakingFeedAdapter` جدا اضافه می‌شود
- خبرهای ناگهانی از منبع feed/API وارد همان ساختار Event می‌شوند
- `IsBreaking=true` و `TimeUtc=now` یا timestamp خبر تنظیم می‌شود

## 8. Time Normalization

همه چیز باید اول به UTC normalize شود.

```text
Source Time + Source Offset → UTC → Broker Time → Chart Object Time
```

### ورودی‌های زمانی

- `InpSourceGMTOffsetHours`
- `InpBrokerGMTOffsetHours`
- `InpAutoDetectBrokerGMT`
- `InpManualBrokerOffsetOverride`
- `InpDayStartMode`

## 9. Auto Broker GMT Detection

ایده:

1. ساعت `TimeCurrent()` بروکر گرفته شود
2. ساعت `TimeGMT()` گرفته شود
3. اختلاف گرد شده محاسبه شود
4. اگر اختلاف منطقی بود، offset اتوماتیک فعال شود
5. اگر اختلاف غیرعادی بود، input دستی اولویت بگیرد

قانون:

```text
if AutoDetectBrokerGMT=true:
    BrokerOffset = round((TimeCurrent - TimeGMT) / 3600)
else:
    BrokerOffset = InpBrokerGMTOffsetHours
```

## 10. Cache Model

فایل cache پیشنهادی:

```text
MQL5/Files/GartalTerminal/cache/calendar_YYYYMMDD.json
```

رفتار:

- اگر fetch موفق بود، cache update شود
- اگر fetch fail شد، cache امروز load شود
- اگر cache قدیمی‌تر از X ساعت بود، داشبورد warning بدهد
- هیچ‌وقت fetch fail نباید indicator را crash کند

## 11. Refresh Policy

پیشنهاد:

```text
Normal refresh: every 5 minutes
Near event: every 30 seconds
After release: every 30 seconds for 5 minutes
Market closed: every 15 minutes
```

## 12. Parser Hardening

Parser باید این موارد را تحمل کند:

- فاصله و newline زیاد
- تغییر کوچک در class name
- نبودن actual/forecast/previous
- eventهای all day
- tentative time
- revised previous
- چند خبر در یک ساعت
- ارزهای غیراستاندارد

## 13. Versioned Adapter

هر adapter باید version داشته باشد:

```text
GT_FF_HTML_ADAPTER_VERSION = 1
GT_JSON_API_ADAPTER_VERSION = 1
```

اگر adapter شکست خورد، پیام UI:

```text
DATA SOURCE WARNING: calendar parser failed. Using cache.
```
