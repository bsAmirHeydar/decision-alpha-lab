# Filter and Dashboard Interaction Model

## 1. اصل محصولی

فیلترها فقط نباید در input باشند. کاربر باید هنگام ترید، داخل همان داشبورد بتواند سریع روشن/خاموش کند.

## 2. فیلترهای داخلی

### Currency Buttons

```text
[USD] [EUR] [GBP] [JPY] [CHF] [CAD] [AUD] [NZD] [CNY]
```

کلیک:

- یک کلیک: toggle
- Shift-click یا دکمه جدا: only this
- دکمه Reset: برگشت به input default

### Impact Buttons

```text
[LOW] [MED] [HIGH] [SPEECH] [HOLIDAY] [BREAKING]
```

### Range Buttons

```text
[TODAY] [TOMORROW] [WEEK] [CUSTOM]
```

### Alert Button

```text
[ALERTS ON/OFF]
```

## 3. State Management

داشبورد باید یک state داخلی داشته باشد:

```text
GT_DashboardState
  selectedCurrencies
  selectedImpacts
  rangeMode
  alertEnabled
  compactMode
  onlyCurrentSymbol
```

این state از input اولیه ساخته می‌شود، ولی بعد از کلیک کاربر روی buttonها override می‌شود.

## 4. Persistence

برای نسخه حرفه‌ای، state می‌تواند با GlobalVariables ذخیره شود:

```text
GTNEWS_STATE_<account>_<symbol>
```

نسخه ساده: state فقط در runtime.

## 5. Dashboard Rows

هر ردیف خبر:

```text
Time | Currency | Impact Dot | Title | Values | Countdown | Alert Icon
```

## 6. Row Priority

وقتی جا کم است:

1. خبر بعدی
2. high impact مربوط به symbol
3. high impact عمومی
4. medium مربوط به symbol
5. speech high
6. low
7. holiday

## 7. Status Indicators

```text
LIVE        fetch ok
CACHE       using cache
STALE       cache old
ERROR       source failed
OFFLINE     no internet/cache
```

## 8. UX برای خبرهای ناگهانی

Breaking یا speech high impact باید در بالای dashboard pin شود، حتی اگر sorting معمولی چیز دیگری بگوید.

## 9. Rule برای simplicity

هر دکمه UI باید فقط یک کار کند. هیچ منوی پیچیده‌ای در نسخه اول لازم نیست. Toggleهای مستقیم بهتر از panelهای تو در تو هستند.
