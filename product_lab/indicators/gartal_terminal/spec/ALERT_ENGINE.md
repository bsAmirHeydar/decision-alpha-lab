# Alert Engine — gartal terminal

## 1. هدف

هشدار باید دقیق، کم‌تکرار و قابل اعتماد باشد. بدترین حالت محصول خبری این است که alertها دیر، تکراری یا اشتباه باشند.

## 2. Alert Types

```text
PRE_60M
PRE_30M
PRE_15M
PRE_5M
PRE_1M
AT_RELEASE
AFTER_ACTUAL
SOURCE_FAIL
CACHE_STALE
BREAKING_NOW
```

## 3. کانال‌ها

```text
Popup Alert()
Sound PlaySound()
Push SendNotification()
Email SendMail()
Dashboard Flash
Chart Marker Pulse
```

## 4. Alert Eligibility

هشدار فقط زمانی فعال شود که:

- event فیلتر نشده باشد
- alert برای آن event روشن باشد
- threshold قبلاً sent نشده باشد
- event هنوز معتبر باشد
- در حالت symbol-only، event به symbol مربوط باشد

## 5. Duplicate Prevention

کلید alert:

```text
EventId + AlertType + Account + Symbol
```

این کلید در runtime map نگه داشته می‌شود. برای persistence می‌توان GlobalVariables یا فایل cache استفاده کرد.

## 6. Message Format

```text
gartal terminal | HIGH USD | CPI m/m | 15m remaining | 15:30 Broker
```

برای breaking:

```text
gartal terminal | BREAKING HIGH | USD Speech | now/live risk
```

## 7. Near-release Behavior

اگر خبر کمتر از ۵ دقیقه مانده باشد:

- dashboard row pulse کند
- timeline marker highlight شود
- vertical line ضخیم‌تر شود
- alert اگر روشن است، یک بار صادر شود

## 8. After Actual Behavior

اگر actual/forecast/previous آپدیت شد:

- row status = RELEASED
- actual رنگی شود
- فقط یک alert بعد از actual صادر شود
- اگر actual خالی ماند، بعد از X دقیقه stop polling شود

## 9. Default Alerts

پیشنهاد نسخه فروش:

```text
30m before = on
15m before = on
5m before = on
At release = on
After actual = off by default
Push = off by default
Sound = on
Popup = on
```

## 10. Fail Alerts

اگر منبع داده fail شد، کاربر باید بداند:

```text
Calendar source failed. Using cache from HH:MM.
```

اما این alert نباید هر ۵ دقیقه آزاردهنده تکرار شود. فقط یکبار در هر بازه مشخص.
