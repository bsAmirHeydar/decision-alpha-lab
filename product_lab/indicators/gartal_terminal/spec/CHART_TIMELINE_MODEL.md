# Chart Timeline Model

## 1. هدف

خبرها باید روی زمان چارت قرار بگیرند. کاربر نباید فقط یک جدول ببیند؛ باید «نقشه زمانی ریسک» را در فضای چارت حس کند.

## 2. دو لایه نمایش

### Vertical Event Layer

برای خبرهایی که timestamp آن‌ها داخل محدوده قابل نمایش چارت است.

### Bottom Timeline Layer

برای کل خبرهای آینده روز، حتی اگر سمت راست چارت هنوز کندل ندارد.

## 3. قواعد رسم خط عمودی

Object name:

```text
GT_VLINE_<event_id>
GT_LABEL_<event_id>
```

رنگ:

- high: red
- medium: orange
- low: yellow
- speech: violet overlay
- breaking: red pulse

## 4. قواعد timeline پایین

Object name:

```text
GT_TL_AXIS
GT_TL_DOT_<event_id>
GT_TL_TEXT_<event_id>
```

Timeline به صورت screen-space object ساخته می‌شود، نه الزاماً فقط time-price. این کار باعث می‌شود خبرهای انتهای روز حتی جلوتر از چارت هم قابل نمایش باشند.

## 5. Mapping زمان به موقعیت افقی

```text
x = timeline_left + ((event_time - day_start) / (day_end - day_start)) * timeline_width
```

اگر range today باشد:

```text
day_start = broker date 00:00
day_end = broker date 23:59
```

اگر custom باشد:

```text
range_start = now - daysBack
range_end = now + daysForward
```

## 6. جلوگیری از overlap

اگر دو خبر نزدیک هم هستند:

- dotها روی محور بمانند
- labelها در دو ردیف alternate شوند
- اگر هنوز overlap بود، label کوتاه شود
- در حالت compact فقط currency+impact نمایش داده شود

## 7. خبرهای گذشته

- dim شوند
- اگر بیش از hidePastAfterMinutes گذشته، حذف شوند
- در dashboard optional بمانند

## 8. خبر بعدی

خبر بعدی باید:

- glow داشته باشد
- countdown برجسته داشته باشد
- اگر relevant به symbol است، حاشیه سفید/روشن بگیرد

## 9. Timeframe Change

در `OnChartEvent` یا `OnCalculate` باید redraw سبک انجام شود. Objectها نباید روی timeframe جدید جا بمانند یا duplicate شوند.

## 10. Clean Up

در OnDeinit اگر `InpCleanObjectsOnDeinit=true` تمام objectهای با prefix `GT_` حذف شوند.
