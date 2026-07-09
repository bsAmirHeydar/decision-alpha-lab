# Algorithm Architecture — gartal terminal

## 1. جریان کلی

```text
OnInit
  ├─ read inputs
  ├─ detect broker GMT
  ├─ initialize UI objects
  ├─ load cache
  ├─ set timer
  └─ first refresh

OnTimer
  ├─ check refresh schedule
  ├─ fetch calendar if needed
  ├─ parse and normalize events
  ├─ filter events
  ├─ update dashboard
  ├─ draw timeline
  ├─ draw event lines
  └─ process alerts

OnChartEvent
  ├─ handle filter buttons
  ├─ toggle alerts
  ├─ open event card
  └─ refresh UI

OnDeinit
  ├─ remove GT_* objects
  └─ save state/cache
```

## 2. ماژول‌ها

### 2.1 Input Controller

مسئول خواندن input و ساخت config داخلی.

خروجی:

```text
GT_Config
```

### 2.2 Data Client

مسئول fetch داده.

تابع‌ها:

```text
FetchToday()
FetchRange(daysBack, daysForward)
FetchFromCache()
SaveCache()
```

### 2.3 Parser

مسئول تبدیل raw HTML/JSON به event.

تابع‌ها:

```text
ParseCalendar(raw)
ParseImpact(rawRow)
ParseCurrency(rawRow)
ParseEventTime(rawRow)
ParseActualForecastPrevious(rawRow)
ClassifyEventType(title, impact)
```

### 2.4 Normalizer

مسئول زمان و فیلدهای استاندارد.

```text
NormalizeToUtc()
ConvertUtcToBroker()
BuildEventId()
BuildRowHash()
```

### 2.5 Filter Engine

فیلترها را اعمال می‌کند.

```text
FilterByCurrency()
FilterByImpact()
FilterByDateRange()
FilterByCurrentSymbol()
FilterByEventType()
FilterByDashboardState()
```

### 2.6 Relevance Engine

تشخیص می‌دهد خبر به چارت فعلی مربوط است یا نه.

مثال:

```text
EURUSD → EUR, USD
GBPJPY → GBP, JPY
XAUUSD → USD + global high risk
US30 → USD + global high risk
BTCUSD → USD + global risk if enabled
```

### 2.7 UI Renderer

مسئول objectهای گرافیکی.

```text
RenderDashboard()
RenderFilterButtons()
RenderTimeline()
RenderVerticalLines()
RenderEventCards()
RenderSourceStatus()
```

### 2.8 Alert Engine

مسئول جلوگیری از alert تکراری و ارسال هشدار.

```text
ShouldAlert(event, threshold)
MarkAlertSent(event, threshold)
SendPopup()
SendSound()
SendPush()
SendEmail()
```

## 3. ساختار داده پیشنهادی

```cpp
struct GT_NewsEvent
{
   string id;
   datetime time_utc;
   datetime time_broker;
   string currency;
   int impact;
   string title;
   string actual;
   string forecast;
   string previous;
   int event_type;
   bool is_tentative;
   bool is_speech;
   bool is_holiday;
   bool is_breaking;
   bool is_relevant;
   bool is_released;
   string source;
   string raw_hash;
};
```

## 4. اولویت رخدادها

برای sorting و نمایش:

```text
1. خبر بعدی high impact relevant
2. خبرهای high impact آینده
3. خبرهای medium relevant
4. speech قرمز
5. breaking
6. low impact
7. holiday
```

## 5. جلوگیری از duplicate

EventId باید از این‌ها ساخته شود:

```text
Date + Time + Currency + NormalizedTitle
```

اگر actual/forecast آپدیت شد، EventId عوض نشود؛ فقط row hash تغییر کند.

## 6. منطق alert

برای هر event یک alert-state نگه می‌داریم:

```text
eventId + thresholdKey → sent/not sent
```

مثال:

```text
USD_CPI_20260709_1530_PRE_15M = sent
USD_CPI_20260709_1530_RELEASE = not_sent
```

## 7. منطق رسم آینده روی چارت

چالش: چارت کندل آینده ندارد. راه‌حل‌ها:

### روش A — Object with time beyond current bar

بسیاری از objectهای MT5 می‌توانند با timestamp آینده رسم شوند، اگر chart shift/space فعال باشد.

### روش B — Fixed bottom dashboard timeline

به جای وابستگی کامل به محور کندل آینده، یک timeline مستقل داخل پنل پایین رسم می‌شود.

### روش C — Hybrid

- vertical line برای خبرهایی که timestampشان داخل محدوده قابل نمایش است
- bottom timeline برای کل باقی روز

پیشنهاد محصول: Hybrid.

## 8. Fail-Safe Rules

- اگر fetch fail شد، cache load شود
- اگر cache نبود، UI پیام دهد
- اگر parser fail شد، indicator unload نشود
- اگر alert engine خطا داد، UI و chart drawing ادامه یابد
- اگر تعداد objectها زیاد شد، clean redraw انجام شود

## 9. Performance Rules

- objectها با prefix مشخص ساخته شوند
- قبل از redraw کامل، فقط objectهای لازم update شوند
- refresh بی‌دلیل هر tick ممنوع است
- fetch فقط روی timer انجام شود
- alert check سبک باشد
- dashboard pagination داشته باشد

## 10. Testing Scenarios

- روز بدون خبر
- روز NFP
- روز FOMC
- چند خبر در یک ساعت
- خبر tentative
- speech بدون actual/forecast
- تغییر ساعت تابستانی broker
- قطع اینترنت
- تغییر symbol
- تغییر timeframe
- refresh manual
- بروکر با GMT offset غیرعادی
