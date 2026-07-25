# EXP0013 — Astro Path Cleanliness Screen Guide

## هدف این صفحه

این دمو هیچ معامله‌ای باز نمی‌کند. هدفش فقط این است که در Visual Tester یا اجرای live، روی هر کندل ببینیم وضعیت آسمان از نظر **تمیزی مسیر** چه شکلی است.

ما در این فاز دنبال جهت نیستیم. سؤال این نیست که آسترولوژی Buy می‌دهد یا Sell. سؤال این است:

```text
وقتی یک execution جداگانه سیگنال داد، آیا این وضعیت آسمان می‌تواند مسیر را تمیزتر، کم‌پولبک‌تر، سریع‌تر و قابل رولت‌تر کند؟
```

پس این Expert فقط یک ابزار مشاهده و کالیبراسیون است.

---

## فایل‌های مربوط

```text
mql5/Include/Research/DAL_AstroPathCleanlinessMetrics.mqh
mql5/Experts/Research/EXP0013_AstroPathCleanlinessMetrics_Demo.mq5
contexts/legacy/lab_experiments/EXP0013_astro_feature_store/ASTRO_PATH_CLEANLINESS_SCREEN_GUIDE.md
```

فایل CSV باید قبلاً با Python ساخته شده باشد و داخل این مسیر در ترمینال متاتریدر قرار بگیرد:

```text
<META_TRADER_DATA_FOLDER>/MQL5/Files/astro/...
```

مثلاً:

```text
MQL5/Files/astro/astro_XAUUSD_M1_202401_mql.csv
```

---

## اجرای دمو

روی چارت یا Visual Tester این Expert را اجرا کن:

```text
mql5/Experts/Research/EXP0013_AstroPathCleanlinessMetrics_Demo.mq5
```

inputهای مهم:

```text
InpAstroCsvFile         = astro\astro_XAUUSD_M1_202401_mql.csv
InpBrokerGmtOffsetHours = 2.0
InpReadTimeframe        = PERIOD_M1
InpRequireExactBarTime  = true
InpReadOnlyOnNewBar     = true
InpValidateUtcOffset    = true
```

قانون زمان:

```text
UTC = broker_time - InpBrokerGmtOffsetHours
```

اگر ساعت بروکر UTC+2 است، offset باید `2.0` باشد. اگر UTC+3 است، باید `3.0` باشد. اگر این عدد غلط باشد، نقشه آسمان به کندل اشتباه وصل می‌شود و کل تحقیق خراب می‌شود.

---

# فلسفه‌ی متریک‌ها

این ماژول وضعیت خام آسترولوژی را به چند محور قابل تست تبدیل می‌کند:

```text
Flow
Impulse
Friction
Pressure
Transition
MoonTempo
SaturnDrag
```

همه امتیازها از 0 تا 100 هستند.

عدد بالا همیشه خوب نیست. معنی هر محور فرق دارد.

---

## 1. Flow

`Flow` یعنی روانی هندسه آسمان.

در پروژه ما این را این‌طور می‌خوانیم:

```text
Flow بالا = فرضیه‌ی حرکت نرم‌تر، پولبک کمتر، ادامه مسیر بهتر
Flow پایین = فرضیه‌ی گیرکردن، حرکت کثیف‌تر، سخت‌تر شدن continuation
```

Flow بیشتر از aspectهای نرم ساخته می‌شود:

```text
trine
sextile
```

جفت‌هایی که در Flow اثر دارند:

```text
sun_moon
venus_mars
moon_venus
moon_jupiter
sun_jupiter
jupiter_saturn
```

Flow به درد این سؤال می‌خورد:

```text
آیا مسیر بعد از سیگنال، نرم و کم‌پولبک‌تر می‌شود؟
```

---

## 2. Impulse

`Impulse` یعنی نیروی حرکت، انفجار، momentum.

در بازار:

```text
Impulse بالا = احتمال حرکت ضربه‌ای، breakout، follow-through سریع‌تر
Impulse پایین = احتمال کم‌تحرکی یا حرکت ضعیف‌تر
```

این امتیاز بیشتر از این‌ها ساخته می‌شود:

```text
Mars speed/state
Mars element
Mars modality
Moon speed
element bias
modality bias
```

برای Donchian، ATR expansion و breakout، Impulse مهم‌تر از Flow خام است.

اما Impulse تنها کافی نیست. اگر Impulse بالا باشد ولی Friction و Pressure هم بالا باشند، حرکت می‌تواند خشن و پر ویک باشد.

حالت مطلوب برای مسیر تمیز:

```text
Impulse mid/high
Friction low
Pressure low/mid
Transition low
```

---

## 3. Friction

`Friction` یعنی اصطکاک مسیر.

در بازار:

```text
Friction بالا = احتمال پولبک، گیرکردن، ویک، delay، fake breakout
Friction پایین = مسیر آزادتر و کم‌مانع‌تر
```

Friction از این مؤلفه‌ها ساخته می‌شود:

```text
SaturnDrag
MercuryDisturbance
Pressure
Transition
```

برای هدف ما، Friction یکی از مهم‌ترین محورهای منفی است. اگر Friction بالا باشد، حتی اگر معامله سود شود، ممکن است مسیرش برای رولت کثیف باشد.

---

## 4. Pressure

`Pressure` یعنی فشار هندسی.

از aspectهای سخت ساخته می‌شود:

```text
conjunction
square
opposition
```

جفت‌های مهم:

```text
mars_saturn
moon_saturn
moon_mars
sun_saturn
sun_mars
jupiter_saturn
sun_moon
```

در بازار:

```text
Pressure بالا = volatility / حرکت شدید / اما احتمال wick و برگشت هم بیشتر
Pressure پایین = آرام‌تر / شاید کم‌حرکت‌تر
Pressure میانی = گاهی برای حرکت تمیز بهتر از فشار خیلی بالا است
```

برای همین در Composite CleanPath، فشار میانی امتیاز بهتری می‌گیرد.

---

## 5. Transition

`Transition` یعنی تغییر فاز.

از این‌ها ساخته می‌شود:

```text
planet ingress near
station near
moon phase boundary near
```

در بازار:

```text
Transition بالا = احتمال تغییر رژیم، رفتار نامطمئن، شروع/پایان فاز، fake move
Transition پایین = وضعیت پایدارتر
```

برای رولت و توالی‌های تمیز، معمولاً Transition پایین مطلوب‌تر است.

---

## 6. MoonTempo

`MoonTempo` یعنی سرعت ماه.

در این تحقیق ماه را به عنوان tempo کوتاه‌مدت نگاه می‌کنیم:

```text
MoonTempo بالا = ریتم سریع‌تر
MoonTempo پایین = ریتم کندتر
```

این به خودی خود جهت نمی‌دهد. فقط کمک می‌کند بفهمیم آیا وضعیت کوتاه‌مدت می‌تواند با حرکت سریع‌تر یا کندتر همراه باشد.

---

## 7. SaturnDrag

`SaturnDrag` یعنی کشش و مقاومت زحلی.

از این‌ها ساخته می‌شود:

```text
Saturn station
Saturn retrograde
Saturn slow
Saturn hard aspects with Mars/Moon/Sun/Jupiter
```

در بازار:

```text
SaturnDrag بالا = احتمال تأخیر، فشار ساختاری، پولبک عمیق، گیرکردن
SaturnDrag پایین = مانع ساختاری کمتر
```

برای تمیزی مسیر، SaturnDrag پایین معمولاً مطلوب‌تر است.

---

# Composite Scores

## CleanPath

```text
CleanPath = ترکیبی از Flow، Impulse، کم بودن Friction، فشار متعادل، کم بودن Transition، کم بودن SaturnDrag
```

خوانش:

```text
CleanPath بالا = کاندید مسیر کم‌پولبک‌تر
CleanPath پایین = احتمال مسیر کثیف‌تر یا ضعیف‌تر
```

این مهم‌ترین score برای هدف فعلی است.

---

## CleanImpulse

این یعنی حرکت ضربه‌ای اما نه خیلی کثیف.

```text
CleanImpulse بالا = Impulse خوب + Flow کافی + Friction کنترل‌شده
```

برای Donchian breakout و ATR-based execution مهم است.

---

## SmoothContinuation

این بیشتر برای HA، continuation و مسیرهای نرم است.

```text
SmoothContinuation بالا = Flow بالا + Friction پایین + SaturnDrag پایین
```

---

## BreakoutFollowthrough

این یعنی احتمال follow-through بعد از شکست.

```text
BreakoutFollowthrough بالا = Impulse بالا + Pressure کافی + MoonTempo مناسب + Friction پایین
```

برای Donchian و breakoutها کاربرد دارد.

---

## PullbackRisk

این score منفی است.

```text
PullbackRisk بالا = احتمال MAE بیشتر، برگشت عمیق‌تر، مسیر آزاردهنده‌تر
```

از Friction، Pressure، SaturnDrag، Transition و MercuryDisturbance ساخته می‌شود.

برای رولت، PullbackRisk بالا خطرناک است حتی اگر جهت درست باشد.

---

## ChopRisk

این هم منفی است.

```text
ChopRisk بالا = احتمال رنج، fake move، دیر رسیدن به هدف، مسیر بی‌کیفیت
```

از Friction، Transition، SaturnDrag و پایین بودن Flow ساخته می‌شود.

---

# Regimeها

ماژول در نهایت یک `astro_path_regime` می‌دهد:

```text
clean_flow
clean_impulse
dirty_impulse
drag_chop
transition
soft_flow
neutral
```

## clean_flow

مسیر روان، مناسب ادامه مسیر، کم‌اصطکاک.

برای HA و continuation جذاب‌تر است.

## clean_impulse

حرکت ضربه‌ای با اصطکاک کنترل‌شده.

برای Donchian breakout و ATR expansion جذاب‌تر است.

## dirty_impulse

حرکت ممکن است شدید باشد، اما مسیر ممکن است کثیف، پر ویک و پرپولبک باشد.

برای رولت خطرناک است.

## drag_chop

کشش و اصطکاک بالا. احتمال رنج/تاخیر/گیرکردن بیشتر.

## transition

وضعیت تغییر فاز. باید با احتیاط خوانده شود.

## soft_flow

حرکت نرم اما شاید کم‌انرژی‌تر.

## neutral

وضعیت ترکیبی یا نامشخص. باید با داده بازار و Distribution Engineering تصمیم گرفت.

---

# رشته‌های فیچر

ماژول سه رشته می‌سازد.

## astro_path_key

برای دسته‌بندی کلی مسیر:

```text
astro_path=flow_high|impulse_mid|friction_low|pressure_mid|transition_low|moon_high|saturn_drag_low|regime_clean_flow
```

## clean_gate_key

برای gate یا فیلتر تمیزی مسیر:

```text
clean_gate=clean_high|pb_low|chop_low|ms_none|sm_tri_close_app|elem_fire_air|mod_cardinal
```

## diagnostic_key

برای تحلیل جزئی‌تر:

```text
astro_diag=phase_waxing|moon_decl_north|mars_D_fast_fire|saturn_R_slow_water|mercury_D_normal_air|...
```

برای شروع، در Distribution Engineering بهتر است اول `astro_path_key` و `clean_gate_key` را تست کنیم. `diagnostic_key` خیلی جزئی‌تر است و ممکن است sample size را له کند.

---

# چطور در چارت بخوانیم؟

وقتی Visual Tester را اجرا می‌کنی، روی هر کندل این بخش‌ها را می‌بینی:

```text
PATH AXES 0..100
COMPOSITE PATH SCORES
KEY BODIES
KEY ASPECTS
FEATURE KEYS
```

اول این‌ها را نگاه کن:

```text
CleanPath
PullbackRisk
ChopRisk
astro_path_regime
```

بعد بازار را نگاه کن:

```text
آیا وقتی CleanPath بالا و PullbackRisk پایین است، مسیر واقعاً تمیزتر است؟
آیا وقتی dirty_impulse یا drag_chop است، حرکت‌ها ویک‌دار و کثیف‌ترند؟
آیا clean_impulse با breakoutهای مستقیم‌تر همزمان می‌شود؟
آیا clean_flow با HA continuation نرم‌تر همزمان می‌شود؟
```

---

# چیزی که باید دستی مشاهده کنی

فعلاً معامله نمی‌کنیم. فقط نگاه می‌کنیم:

```text
1. آیا قبل از حرکت‌های تمیز، CleanPath بالا می‌رود؟
2. آیا قبل از breakoutهای خوب، CleanImpulse یا BreakoutFollowthrough بالا می‌رود؟
3. آیا قبل از پولبک‌های عمیق، PullbackRisk یا SaturnDrag بالا می‌رود؟
4. آیا قبل از رنج و fake move، ChopRisk یا Transition بالا می‌رود؟
5. آیا regimeهای clean_flow و clean_impulse واقعاً رفتار متفاوتی نسبت به neutral دارند؟
```

---

# مرحله بعد

بعد از مشاهده بصری، مرحله علمی این است که همین متریک‌ها را کنار نتایج executionها ثبت کنیم:

```text
entry_time
astro_path_key
clean_path_score
pullback_risk_score
chop_risk_score
MAE_R
MFE_R
path_efficiency
pullback_depth_R
bars_to_target
hit_3R
```

بعد Distribution Engineering می‌گوید کدام astro state واقعاً توزیع مسیر را تمیزتر کرده است.

---

# هشدار علمی

این صفحه هیچ ادعای علیت ندارد.

```text
بالا بودن CleanPath به معنی قطعی بودن مسیر تمیز نیست.
پایین بودن PullbackRisk به معنی نبود پولبک نیست.
این‌ها فقط featureهای قابل تست هستند.
```

ارزش این ماژول فقط وقتی مشخص می‌شود که با داده‌ی مسیر بازار سنجیده شود.
