# AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت

## وضعیت این سند

این سند مرجع فلسفی و مهندسی مسیر بعدی پروژه است.

این سند کد اجرایی نیست.

این سند قرار است قبل از ورود به train، backtest، مدل‌های هوش مصنوعی و execution bridge، زبان مشترک ما را ثابت کند.

---

# 1. هدف اصلی

هدف پروژه این نیست که یک هوش مصنوعی کلاسیک روی کندل خام، اندیکاتورهای عمومی، زمان‌بندی‌های مصنوعی یا الگوهای رایج train شود.

هدف این است:

```text
چارچوب اختصاصی ما از بازار
→ تجربه‌های انسانی امیر
→ تعریف رسمی stateها و episodeها
→ labelهای ساختاری
→ الگوریتم‌های جداگانه AI
→ execution intent
→ بک‌تست حرفه‌ای روی MetaTrader 5
→ shadow / paper / live bridge
```

هوش مصنوعی قرار نیست بازار را از صفر تعریف کند.

هوش مصنوعی باید داخل زبان خودمان یاد بگیرد.

زبان ما شامل این‌هاست:

```text
X-axis structure
Y-axis phase
Hook
Rally
F-counting
F1 / F2 / F3
Node context
selected extreme
invalidation
destination
fractal context
optionality
path cleanliness
execution difficulty
paper lifecycle
final decision state
runtime health
```

---

# 2. اصل بنیادین

## AI نباید بیرون از جهان ما فکر کند

ما نمی‌خواهیم AI این چیزها را وارد تصمیم‌گیری کند:

```text
RSI
Moving Average
MACD
ICT label
breakout
confirmation
weakness
trend کلاسیک
raw candle prediction
time horizon مصنوعی
hour / weekday edge
```

این‌ها فعلاً خارج از ontology پروژه‌اند.

اصل ما:

```text
ما ضعف معامله نمی‌کنیم.
ما تأییدیه معامله نمی‌کنیم.
ما شکست معامله نمی‌کنیم.
ما اکستریم‌های انتخاب‌شده‌ای را معامله می‌کنیم که در آن‌ها ساختار X، فاز Y، زمینه فرکتالی و آپشنالیتی هم‌راستا باشند.
```

---

# 3. نقش امیر و نقش AI

## نقش امیر

امیر معمار زبان بازار است.

امیر تعیین می‌کند:

```text
چه چیزی در بازار مهم است
چه چیزی مزخرف و فریبنده است
کدام حالت‌ها از تجربه انسانی ارزش دارند
کجاها باید AI نگاه کند
کجاها نباید نگاه کند
چه فرضیه‌هایی باید تست شوند
چه چیزهایی باید hard rule باشند
چه چیزهایی باید feature باشند
چه چیزهایی باید label یا test باشند
```

## نقش AI

AI قرار نیست جای امیر را بگیرد.

AI باید این کارها را انجام دهد:

```text
در زبان تعریف‌شده توسط امیر یاد بگیرد
هزاران episode را مقایسه کند
ترکیب‌های ساختاری ارزشمند را پیدا کند
setupهای بد را veto کند
setupهای خوب را rank کند
execution template انتخاب کند
cancel / replace policy را بهتر کند
optionality را بهتر exploit کند
```

پس رابطه اصلی:

```text
امیر = طراح جهان و زبان
AI = یادگیرنده، رتبه‌بند، ممیز، و مسیریاب داخل همان جهان
```

---

# 4. تجربه‌های انسانی چطور وارد سیستم می‌شوند؟

تجربه‌های امیر باید به سه شکل وارد سیستم شوند.

## 4.1 Hard Rule

وقتی تجربه قطعی و غیرقابل مذاکره است.

مثال:

```text
اگر Y-phase تغییر کرد، pending order قبلی نباید زنده بماند.
```

تبدیل می‌شود به rule.

## 4.2 Feature

وقتی تجربه مهم است اما همیشه صددرصد نیست.

مثال:

```text
F3 اغلب آخر روند است.
```

این نباید فوراً قانون قطعی شود.

به feature تبدیل می‌شود:

```text
f_type
f3_terminal_candidate
f3_after_extended_rally
f3_parent_alignment
f3_destination_proximity
f3_invalidation_tightness
```

بعد AI و آمار بررسی می‌کنند که در چه contextهایی این تجربه واقعاً درست است.

## 4.3 Label / Test

وقتی تجربه باید اثبات یا رد شود.

مثال:

```text
نگاه فرکتالی لازم است.
```

این تبدیل می‌شود به تست:

```text
fractal_aligned episodes
fractal_conflicted episodes
```

بعد بررسی می‌کنیم:

```text
آیا destination-before-invalidation بهتر شد؟
آیا path cleanliness بهتر شد؟
آیا optionality بهتر آزاد شد؟
آیا realized R بهتر شد؟
```

---

# 5. مسیر تبدیل تجربه به سیستم

هر تجربه باید با این template ثبت شود.

## Experience Template

```text
experience_id:
title:
description:
source:
  manual_experience / observation / chart_replay / backtest / hypothesis

core_claim:
  ادعای اصلی چیست؟

ontology_area:
  X-axis / Y-axis / F-counting / Hook / Rally / Fractal / Optionality / Execution

should_be:
  hard_rule / feature / label / test / execution_policy

required_fields:
  چه fieldهایی باید ساخته شوند؟

expected_effect:
  چه چیزی باید بهتر شود؟
  hit destination?
  lower invalidation?
  cleaner path?
  better R-tail?
  fewer bad fills?
  better cancel/replace?

falsification:
  چه چیزی این تجربه را رد می‌کند؟

notes:
```

هیچ تجربه‌ای نباید فقط در ذهن بماند.

همه باید به field، rule، label یا test تبدیل شوند.

---

# 6. AI دقیقاً کجا کمک می‌کند؟

## 6.1 Opportunity Ranking

AI بین فرصت‌های مجاز رتبه‌بندی می‌کند.

ورودی:

```text
canonical state packet
structural episode context
optionality context
fractal context
```

خروجی:

```text
rank_score
reason_vector
```

کار:

```text
کدام opportunity ارزش بیشتری دارد؟
```

---

## 6.2 Veto Model

AI می‌گوید کدام setup ظاهراً آماده است اما نباید اجرا شود.

خروجی:

```text
ALLOW
VETO
DELAY
```

کار:

```text
حذف setupهای فریبنده
کاهش ورودهای کثیف
کاهش invalidationهای بی‌کیفیت
```

---

## 6.3 Execution Template Selector

AI انتخاب می‌کند با setup چطور رفتار کنیم.

خروجی:

```text
LIMIT_AT_SELECTED_EXTREME
LIMIT_DEEPER_IN_ZONE
WAIT_FOR_RETOUCH
DO_NOT_CHASE
CANCEL_ON_Y_PHASE_CHANGE
REPLACE_IF_NEW_EXTREME_FORMS
```

---

## 6.4 Cancel / Replace Policy

AI یاد می‌گیرد pending order چه زمانی باید زنده بماند، حذف شود یا جابه‌جا شود.

این بخش برای execution bridge بسیار مهم است.

سؤال‌های اصلی:

```text
آیا selected extreme قبلی هنوز معتبر است؟
آیا extreme جدید بهتر ساخته شده؟
آیا Y-phase تغییر کرده؟
آیا destination تغییر کرده؟
آیا invalidation geometry خراب شده؟
آیا opportunity مرده است؟
```

---

## 6.5 Optionality Exploiter

AI دنبال win rate صرف نیست.

AI باید setupهایی را پیدا کند که:

```text
ضررشان محدود است
invalidation تمیز است
destination باز است
اگر جواب بدهند payoff آزاد می‌شود
اگر جواب ندهند سریع و محدود می‌میرند
```

---

# 7. لایه‌های الگوریتمی باید جدا باشند

هیچ AI واحدی نباید همه کارها را با هم انجام دهد.

لایه‌ها باید جدا باشند:

```text
AI_Ranker
AI_Veto
AI_TemplateSelector
AI_CancelPolicy
AI_ReplacePolicy
AI_OptionalityScorer
AI_FractalContextModel
AI_PathQualityModel
AI_ExecutionDifficultyModel
```

هر الگوریتم باید:

```text
input خودش را داشته باشد
output خودش را داشته باشد
manifest خودش را داشته باشد
backtest خودش را داشته باشد
report خودش را داشته باشد
shadow comparison خودش را داشته باشد
```

مدل‌ها نباید قاطی شوند.

---

# 8. Backtest باید حرفه‌ای و ضد اورفیت باشد

هیچ AI یا algorithm بدون این تست‌ها قبول نیست:

## 8.1 Baseline Comparison

هر مدل باید با templateهای rule-based مقایسه شود:

```text
Pure Selected Extreme
Conservative Extreme
Optionality First
Clean Path Candidate
Veto-heavy
```

AI فقط وقتی ارزش دارد که نسبت به baseline چیزی اضافه کند.

## 8.2 Negative Controls

تست‌های ضد فریب:

```text
label shuffle
direction flip
random selected extreme
random entry under same risk
permuted episode order
future leakage check
duplicate episode collapse
```

اگر مدل روی داده‌ی خراب هم خوب بود، مدل garbage است.

## 8.3 Ablation

feature familyها باید حذف شوند و اثرشان بررسی شود:

```text
without X-axis fields
without Y-axis fields
without F-counting fields
without fractal fields
without optionality fields
without lifecycle fields
without execution difficulty fields
```

## 8.4 Structural OOS

تست خارج از نمونه فقط تاریخی نیست.

باید از نظر ساختاری هم جدا باشد:

```text
unseen F-type mix
unseen Hook/Rally mix
unseen fractal conflict state
unseen optionality distribution
unseen execution difficulty class
unseen symbol
unseen scale
```

---

# 9. Execution Bridge

## اصل اصلی

AI هرگز مستقیم order نمی‌دهد.

AI فقط intent تولید می‌کند.

```text
AI → ExecutionIntent → Safety Gate → Validator → Broker Adapter
```

نه:

```text
AI → OrderSend
```

## ExecutionIntent

ساختار پیشنهادی:

```text
intent_id
source_type
source_model_id
source_template_id

mode
  BACKTEST / SHADOW / PAPER / LIVE_DISABLED / LIVE

action
  NONE / WATCH / PLACE_LIMIT / PLACE_MARKET / UPDATE_LIMIT / CANCEL / CLOSE

direction
entry_price
stop_price
target_price

episode_id
selected_extreme_id
invalidation_id
destination_id
y_phase_id

rank_score
veto_state
confidence
reason_vector

cancel_policy_id
replace_policy_id
expiry_policy_id

risk_profile_id
execution_permission_state
```

## حالت‌های execution

مسیر باید جداجدا جلو برود:

```text
BACKTEST
SHADOW
PAPER
LIVE_DISABLED
LIVE
```

تا وقتی backtest و shadow و paper قوی نباشند، live ممنوع است.

---

# 10. MetaTrader 5 نقش چیست؟

MetaTrader 5 جای اجرای واقعی بک‌تست و paper/live bridge است.

اما مغز تصمیم‌گیری باید modular باشد.

ساختار مطلوب:

```text
MQL5 Engine:
  market anatomy
  state extraction
  execution simulator
  broker adapter
  safety gate
  CSV/bridge IO

External AI / Research:
  training
  model comparison
  anti-overfit tests
  reports
  model registry

Bridge:
  CSV / JSON / file-based / later socket/API
```

در فاز اول، ساده‌ترین bridge:

```text
MQL5 exports datasets as CSV
Python trains and evaluates models
Python writes model_signal.csv
MQL5 reads model_signal.csv
MQL5 converts it to ExecutionIntent
```

---

# 11. مسیر اجرایی از اینجا به بعد

## Step 1 — Experience Capture Document

ثبت تجربه‌های امیر با template رسمی.

خروجی:

```text
docs/ai_execution/EXPERIENCE_CAPTURE_LOG_FA.md
```

## Step 2 — Canonical State Packet v1

ساخت زبان feature رسمی پروژه.

خروجی:

```text
canonical_state_packet_v1.csv
```

## Step 3 — Structural Episode Builder v1

ساخت episode از تولد تا مرگ فرصت.

خروجی:

```text
structural_episode_v1.csv
```

## Step 4 — Structural Label Engine v1

ساخت labelهای outcome ساختاری.

خروجی:

```text
structural_labels_v1.csv
```

## Step 5 — Baseline Template Backtests

اجرای templateهای rule-based.

خروجی:

```text
baseline_template_backtest_report.csv
```

## Step 6 — Anti-Overfit Lab

آزمایش‌های ضد overfit.

خروجی:

```text
anti_overfit_report.csv
```

## Step 7 — Algorithm Layer Contracts

تعریف contract جدا برای هر AI layer.

خروجی:

```text
algorithm_contracts/
  ranker_contract.md
  veto_contract.md
  template_selector_contract.md
  cancel_policy_contract.md
  replace_policy_contract.md
  optionality_scorer_contract.md
```

## Step 8 — ExecutionIntent Contract

تعریف intent مشترک برای backtest, shadow, paper, live.

خروجی:

```text
execution_intent_contract_v1.md
```

## Step 9 — Backtest Execution Simulator

اجرای intentها در بک‌تست ساختاری.

## Step 10 — AI Training Loop

مدل‌ها جداگانه train و مقایسه می‌شوند.

## Step 11 — Shadow Mode

AI فقط نظر می‌دهد؛ روی اجرا اثر ندارد.

## Step 12 — Paper Mode

AI اجازه اثر روی paper دارد.

## Step 13 — Live Gate

فقط بعد از اثبات کامل.

---

# 12. سؤال‌هایی که باید از امیر پرسیده شود

این بخش برای جلسات بعدی است.

## درباره F-counting

```text
F1 دقیقاً چه زمانی معتبر است؟
F2 چه چیزی را ثابت می‌کند؟
F3 چرا و کجا terminal candidate است؟
F3 چه زمانی ادامه‌دهنده است نه پایان‌دهنده؟
چه چیزی F3 را invalid می‌کند؟
آیا F3 در parent scale هم باید دیده شود؟
```

## درباره Hook / Rally

```text
Hook دقیقاً چه زمانی زنده است؟
Hook چه زمانی می‌میرد؟
Rally چه زمانی کامل است؟
تغییر Y-phase دقیقاً چه اثری روی pending order دارد؟
```

## درباره X-axis

```text
selected extreme دقیقاً چطور انتخاب می‌شود؟
چه چیزی extreme را بهتر از extreme دیگر می‌کند؟
invalidation باید کجا باشد؟
destination باید چطور انتخاب شود؟
اگر destination عوض شد، order چه شود؟
```

## درباره فرکتال

```text
کدام scaleها برای تصمیم مهم‌اند؟
alignment یعنی دقیقاً چه؟
conflict یعنی دقیقاً چه؟
اگر current scale خوب باشد ولی parent مخالف باشد چه کنیم؟
اگر child scale entry بدهد اما parent destination بسته باشد چه کنیم؟
```

## درباره optionality

```text
اختیار خوب یعنی چه؟
risk کوچک کافی است یا destination هم باید باز باشد؟
چه حالتی payoff را آزاد می‌کند؟
چه حالتی فقط روی کاغذ R خوب دارد اما executable نیست؟
```

## درباره execution

```text
چه زمانی limit بگذاریم؟
چه زمانی market مجاز است؟
چه زمانی pending order باید cancel شود؟
چه زمانی باید replace شود؟
چه زمانی باید به هیچ وجه chase نکنیم؟
```

## درباره AI

```text
اولین الگوریتمی که می‌خواهیم تست کنیم کدام است؟
Ranker؟
Veto؟
Template Selector؟
Cancel Policy؟
Optionality Scorer؟
کدام تجربه انسانی باید اول test شود؟
```

---

# 13. اصل نهایی

این پروژه AI-first نیست.

این پروژه ontology-first است.

```text
اول زبان خودمان
بعد episode
بعد label
بعد baseline
بعد ضد اورفیت
بعد AI
بعد execution intent
بعد backtest
بعد shadow
بعد paper
بعد live
```

AI فقط وقتی ارزش دارد که داخل زبان خودمان، نتیجه را بهتر کند.

