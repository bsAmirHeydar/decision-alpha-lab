# Inputs Reference — gartal terminal

## 1. Data Source Inputs

```text
InpDataSourceMode = ForexFactoryDirect / JsonApiBridge / CacheOnly
InpForexFactoryUrl = https://www.forexfactory.com/calendar
InpUseCache = true
InpCacheMinutes = 5
InpRefreshMinutes = 5
InpRetryOnFail = true
InpMaxRetryCount = 2
```

## 2. Date Range Inputs

```text
InpDateRangeMode = Today / Tomorrow / ThisWeek / Custom
InpDaysBack = 0
InpDaysForward = 0
InpShowPastEvents = true
InpDimPastEvents = true
InpHidePastAfterMinutes = 240
```

پیش‌فرض:

```text
Today only
DaysBack = 0
DaysForward = 0
```

## 3. Currency Inputs

```text
InpCurrencies = USD,EUR,GBP,JPY,CHF,CAD,AUD,NZD,CNY
InpAutoDetectSymbolCurrencies = true
InpShowOnlySymbolCurrencies = false
InpHighlightSymbolCurrencies = true
InpIncludeUsdForGoldAndIndices = true
```

## 4. Impact Inputs

```text
InpShowLowImpact = false
InpShowMediumImpact = true
InpShowHighImpact = true
InpShowHoliday = false
InpShowSpeech = true
InpShowTentative = true
InpShowBreaking = true
```

## 5. Time Inputs

```text
InpAutoDetectBrokerGMT = true
InpBrokerGMTOffsetHours = 0
InpSourceGMTOffsetHours = 0
InpDisplayTimeMode = BrokerTime / UTC / LocalComputer
InpShowBrokerGMTOnDashboard = true
InpDSTAdjustmentMode = Auto / Manual / Off
```

## 6. Dashboard Inputs

```text
InpShowDashboard = true
InpDashboardMode = Compact / Full / ProTerminal / Stealth
InpDashboardCorner = RightUpper
InpDashboardX = 20
InpDashboardY = 30
InpDashboardWidth = 420
InpDashboardRows = 8
InpEnableDashboardFilters = true
InpFontName = Segoe UI
InpFontSize = 9
InpUseDarkGlassTheme = true
```

## 7. Chart Drawing Inputs

```text
InpShowVerticalLines = true
InpShowTimeline = true
InpTimelinePosition = Bottom
InpTimelineHeight = 42
InpShowEventLabels = true
InpLabelMode = Short / Full / CurrencyOnly
InpProjectFutureEvents = true
InpMaxEventsOnChart = 30
InpCleanObjectsOnDeinit = true
```

## 8. Alert Inputs

```text
InpEnableAlerts = true
InpAlertPopup = true
InpAlertSound = true
InpAlertPush = false
InpAlertEmail = false
InpAlertSoundFile = alert.wav
InpAlertHighOnly = false
InpAlertSymbolCurrenciesOnly = true
InpAlertBefore60 = false
InpAlertBefore30 = true
InpAlertBefore15 = true
InpAlertBefore5 = true
InpAlertBefore1 = false
InpAlertAtRelease = true
InpAlertAfterActual = true
InpRepeatAlert = false
```

## 9. UI Color Inputs

```text
InpColorHighImpact
InpColorMediumImpact
InpColorLowImpact
InpColorHoliday
InpColorSpeech
InpColorBreaking
InpColorPastEvent
InpColorNextEvent
InpColorDashboardBg
InpColorTextPrimary
InpColorTextSecondary
InpColorBorder
```

## 10. Developer Inputs

```text
InpDebugMode = false
InpLogRawResponse = false
InpLogParserRows = false
InpUseSampleData = false
InpForceCacheOnly = false
InpObjectPrefix = GT_
```

## 11. License Inputs برای نسخه فروش

```text
InpLicenseKey = ""
InpLicenseEmail = ""
InpLicenseMode = Online / Offline / Trial
InpHideLicenseInputs = false in dev, true in release if needed
```

## 12. اصل ساده‌سازی

تمام inputها باید در گروه‌های واضح باشند:

```text
01 Data Source
02 Time and Broker GMT
03 Currency Filter
04 Impact Filter
05 Dashboard
06 Chart Lines and Timeline
07 Alerts
08 Theme
09 Advanced / Debug
```

قانون: کاربر عادی فقط با ۵ input اول کارش راه بیفتد؛ inputهای پیچیده برای advanced باشد.
