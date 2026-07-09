# UI / UX Design System — gartal terminal

## 1. جهت هنری

حس محصول باید شبیه «ترمینال ماکرو حرفه‌ای» باشد، نه یک اندیکاتور شلوغ رایگان.

کلمات کلیدی:

- luxury terminal
- dark glass
- neon accent
- minimal dense information
- trading desk feel
- high contrast
- clean hierarchy

## 2. ساختار UI

### 2.1 داشبورد اصلی

مکان پیشنهادی: گوشه بالا راست چارت.

بخش‌ها:

```text
┌──────────────────────────────────────────────┐
│ gartal terminal                    LIVE ●   │
│ Today: 09 Jul 2026 | Broker GMT: +3         │
├──────────────────────────────────────────────┤
│ Next High Impact                             │
│ 15:30 USD  CPI m/m                  in 42m   │
├──────────────────────────────────────────────┤
│ Time   Cur  Impact  Event        A/F/P       │
│ 12:00  EUR  MED     ECB Speech   -/-/-       │
│ 15:30  USD  HIGH    CPI m/m      -/0.2/0.1   │
│ 17:00  USD  HIGH    Fed Chair    -/-/-       │
└──────────────────────────────────────────────┘
```

### 2.2 پنل فیلتر داخلی

فیلترها باید با object button داخلی کنترل شوند:

```text
[USD] [EUR] [GBP] [JPY] [CHF] [CAD] [AUD] [NZD] [CNY]
[LOW] [MED] [HIGH] [SPEECH] [HOLIDAY] [BREAKING]
[AUTO SYMBOL] [TODAY] [ALERTS ON]
```

هر دکمه سه حالت دارد:

- فعال: روشن، border واضح
- غیرفعال: dim
- locked: برای نسخه trial یا وابسته به license

### 2.3 خط زمانی پایین چارت

خط زمانی باید پایین چارت و نزدیک margin باشد، نه وسط کندل‌ها. ساختار:

```text
──────●──────────────●────────────────●──────
     EUR MED        USD HIGH         USD HIGH
     12:00          15:30            17:00
```

قانون:

- فقط خبرهای داخل بازه نمایش داده شوند
- خبرهای گذشته dim شوند
- خبر بعدی glow داشته باشد
- high impact ضخیم‌تر/درخشان‌تر باشد

### 2.4 خطوط عمودی خبر

هر خبر می‌تواند یک vertical line داشته باشد:

- `GT_VLINE_<event_id>`
- رنگ بر اساس impact
- line style: dashed برای medium، solid برای high، dotted برای low
- width: high=2/3، medium=1/2، low=1
- label بالا یا پایین کندل، با جلوگیری از هم‌پوشانی

### 2.5 Event card

وقتی کاربر روی خبر کلیک کند یا موس نزدیک object باشد، کارت کوتاه نمایش داده شود:

```text
USD | HIGH
CPI m/m
Time: 15:30 Broker
Forecast: 0.2 | Previous: 0.1
Alert: 15m, 5m, Release
```

## 3. رنگ‌ها

رنگ‌ها باید input داشته باشند، اما default پیشنهادی:

```text
High Impact      = Crimson / Red
Medium Impact    = Amber / Orange
Low Impact       = Yellow / Soft Gold
Holiday          = Gray
Speech           = Violet / Blue
Breaking         = Hot Red + Pulse
Past Event       = Dim Gray
Next Event       = White Glow
Dashboard BG     = Dark translucent
Text Primary     = White
Text Secondary   = Light Gray
Border           = Subtle Neon
```

## 4. حالت‌های UI

### Compact Mode

برای اسکالپرها:

- فقط next event
- ۵ خبر آینده
- فقط currency/impact/time/title کوتاه

### Full Mode

برای تحلیلگرها:

- actual/forecast/previous
- status
- alert state
- source status
- last refresh

### Stealth Mode

برای چارت تمیز:

- فقط timeline پایین
- فقط high impact
- no dashboard

### Pro Terminal Mode

نسخه کامل:

- dashboard full
- timeline
- vertical lines
- alert bar
- filter buttons

## 5. قواعد خوانایی

- متن نباید روی کندل بیفتد
- داشبورد باید anchor و margin input داشته باشد
- اگر تعداد خبرها زیاد شد، pagination داخلی یا scroll-like page button داشته باشد
- title خبر باید کوتاه‌سازی شود اما با hover/card کامل شود
- خبرهای مربوط به symbol فعلی باید برجسته‌تر شوند

## 6. رفتار روی چارت‌های مختلف

### EURUSD

- EUR و USD highlight
- خبرهای سایر ارزها فقط اگر filter all روشن باشد

### XAUUSD

- USD highlight اصلی
- High impact global/speech/breaking highlight ثانویه

### US30 / NAS100 / SPX

- USD و breaking/speech مهم‌تر

### Cross Pair مثل EURJPY

- EUR و JPY highlight

## 7. Anti-Clutter Rules

اگر تعداد خبرها بیشتر از ظرفیت داشبورد شد:

1. High impact همیشه بماند
2. Medium بعدی‌ها بماند
3. Low حذف/فشرده شود
4. Holiday فقط در حالت full
5. Speeches اگر high/red باشند حفظ شوند

## 8. Micro-interactions

- خبر بعدی می‌تواند subtle pulse داشته باشد
- refresh indicator باید کوچک باشد
- alert armed icon کنار هر خبر نمایش داده شود
- در زمان نزدیک خبر، countdown رنگش تغییر کند

قانون رنگ countdown:

```text
> 60m     neutral
60-30m    calm
30-15m    warning
15-5m     strong warning
<5m       danger
release   flash once
```
