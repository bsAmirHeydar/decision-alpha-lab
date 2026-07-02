# AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2

## وضعیت سند

این سند مشخص می‌کند برای استفاده از تجربه‌ی اکستریم L2، چه لایه‌های الگوریتمی و هوش مصنوعی لازم است.

اصل مهم:

```text
هیچ مدل واحدی نباید همه‌چیز را تصمیم بگیرد.
هر مدل باید وظیفه‌ی جدا، ورودی جدا، خروجی جدا، تست جدا و گزارش جدا داشته باشد.
```

AI در این سیستم predictor خام نیست.

AI این کارها را انجام می‌دهد:

```text
کیفیت اکستریم را می‌سنجد.
سناریوهای buy/sell را وزن می‌دهد.
Hook/Rally ambiguity را مدیریت می‌کند.
F3 terminal/continuation را تشخیص می‌دهد.
فرکتال parent/current/child را وارد تصمیم می‌کند.
هزینه اجرا و spread را لحاظ می‌کند.
limit/cancel/replace/hedge را route می‌کند.
```

---

# 1. لایه صفر — Deterministic Ontology Builder

این AI نیست.

این لایه باید کاملاً rule-based و قابل تکرار باشد.

کارش:

```text
ساخت fieldهای رسمی از چارت
```

خروجی:

```text
canonical_state_packet_v1.csv
extreme_opportunity_dataset_v1.csv
```

fieldهای مهم:

```text
anchor_node_id
anchor_node_level
anchor_node_unreached
cycle_completion_ratio
extreme_zone_touched
entry_candidate
stop_candidate
destination_candidate
spread_to_risk_ratio
hook_hypothesis
rally_hypothesis
bullish_case
bearish_case
fractal_context
```

چرا لازم است؟

چون AI نباید خودش مفهوم اکستریم را از raw candle کشف کند.

ما مفهوم را می‌سازیم، AI کیفیت آن را یاد می‌گیرد.

---

# 2. Extreme Quality Model

## هدف

تشخیص اینکه یک اکستریم L2 واقعاً ارزش limit entry دارد یا نه.

## ورودی

```text
anchor_node_level
anchor_node_unreached
cycle_completion_ratio
extreme_zone_relation
distance_to_invalidation
distance_to_destination
raw_rr_like
effective_rr_after_spread
spread_to_risk_ratio
destination_openness
fractal_alignment_state
hook_rally_context
scenario_quality
```

## خروجی

```text
extreme_quality_score
ALLOW / VETO / DELAY
reason_vector
```

## الگوریتم‌های قابل استفاده

### 2.1 Rule Score Baseline

ابتدا یک امتیاز rule-based می‌سازیم.

مثلاً:

```text
L2 unreached مثبت
cycle late مثبت
spread_to_risk پایین مثبت
destination باز مثبت
fractal conflict منفی
```

مزیت:

```text
شفاف، ساده، قابل مقایسه
```

### 2.2 Monotonic Tree Model

مدل درختی با محدودیت‌های منطقی.

مثلاً:

```text
هرچه spread_to_risk بیشتر، کیفیت نباید بهتر شود.
هرچه destination_distance بیشتر، اگر invalidation ثابت باشد، optionality بهتر می‌شود.
```

مزیت:

```text
ضد overfitتر از مدل آزاد
قابل توضیح‌تر
```

### 2.3 Ranking Model

به‌جای پیش‌بینی win/loss، اکستریم‌ها را نسبت به هم rank می‌کند.

مناسب وقتی چند opportunity همزمان داریم.

---

# 3. Dual Scenario Ranker

## هدف

ساخت و رتبه‌بندی همزمان bullish و bearish case.

## ورودی

```text
bullish_case_features
bearish_case_features
bullish_extreme_quality
bearish_extreme_quality
fractal_support_for_bull
fractal_support_for_bear
execution_cost_bull
execution_cost_bear
```

## خروجی

```text
bullish_rank_score
bearish_rank_score
scenario_balance_state
LONG_ONLY / SHORT_ONLY / BOTH_WATCH / BOTH_LIMIT_ALLOWED / NO_TRADE_AMBIGUOUS
```

## الگوریتم‌ها

### 3.1 Pairwise Ranker

bullish و bearish را جفتی مقایسه می‌کند.

سؤال:

```text
در این لحظه، کدام سناریو opportunity بهتری دارد؟
```

### 3.2 Multi-Label Scenario Classifier

ممکن است هر دو سناریو زنده باشند.

خروجی می‌تواند همزمان چند label داشته باشد:

```text
bullish_valid = 1
bearish_valid = 1
hedge_candidate = 0/1
```

---

# 4. Hook / Rally Ambiguity Model

## هدف

مدیریت دو interpretation همزمان:

```text
فرض کنیم Hook هستیم.
فرض کنیم Rally هستیم.
```

## ورودی

```text
hook_hypothesis_features
rally_hypothesis_features
f_count_context
node_context
phase_transition_context
fractal_context
```

## خروجی

```text
hook_quality_score
rally_quality_score
hook_rally_dominance_state
ambiguity_class
```

حالت‌ها:

```text
HOOK_DOMINANT
RALLY_DOMINANT
BOTH_ALIVE
BOTH_WEAK
AMBIGUOUS_NO_TRADE
```

## الگوریتم‌ها

### 4.1 Two-Head Model

یک head برای Hook، یک head برای Rally.

هر head کیفیت interpretation خودش را می‌سنجد.

### 4.2 Ambiguity Gate

اگر هر دو ضعیف‌اند یا conflict خطرناک است:

```text
NO_TRADE_AMBIGUOUS
```

---

# 5. F3 Terminal / Continuation Model

## هدف

تشخیص اینکه F3 واقعاً پایان current structure است یا parent scale آن را override می‌کند.

## ورودی

```text
f_type
f_count
f3_terminal_candidate
f3_reversal_attempt_seen
f3_reversal_failed
parent_phase
parent_f_count
parent_destination_open
parent_continuation_energy
current_scale_exhaustion
child_scale_response
```

## خروجی

```text
f3_terminal_score
f3_continuation_pressure_score
parent_override_state
```

حالت‌ها:

```text
F3_TERMINAL_CONFIRMED
F3_TERMINAL_CANDIDATE
F3_CONTINUATION_PRESSURE
PARENT_OVERRIDES_CURRENT_F3
F3_AMBIGUOUS
```

## الگوریتم‌ها

### 5.1 Classification Model

کلاس‌ها را پیش‌بینی می‌کند.

### 5.2 Survival / State-Transition Model

به‌جای horizon زمانی، transition ساختاری را مدل می‌کند:

```text
F3 → reversal confirmed
F3 → reversal failed
F3 → continuation after reversal
F3 → parent override
```

### 5.3 Parent Ablation Test

مدل بدون parent context نباید به همان خوبی باشد.

اگر بدون parent هم همان نتیجه را بدهد، احتمالاً فرکتال واقعاً وارد مدل نشده است.

---

# 6. Fractal Context Model

## هدف

وزن دادن به parent/current/child.

## ورودی

```text
parent_phase
current_phase
child_phase
parent_f_count
current_f_count
child_f_count
parent_destination_open
parent_invalidation_intact
current_extreme_quality
child_activation_quality
```

## خروجی

```text
fractal_alignment_score
fractal_conflict_class
parent_energy_state
child_noise_or_trigger
```

حالت‌ها:

```text
PARENT_SUPPORTS_CURRENT
PARENT_CONFLICTS_CURRENT
PARENT_CONTINUATION_OVERRIDES_CURRENT
CHILD_TRIGGER_ONLY
CHILD_NOISE
FRACTAL_AMBIGUOUS
```

## الگوریتم‌ها

### 6.1 Hierarchical Scoring

برای هر scale امتیاز جدا ساخته می‌شود، بعد ترکیب می‌شود.

### 6.2 Gated Model

parent می‌تواند current signal را downgrade یا block کند.

### 6.3 Contextual Model

مدل یاد می‌گیرد که child چه زمانی trigger است و چه زمانی فقط noise است.

---

# 7. Execution Cost Model

## هدف

تشخیص اینکه spread و هزینه اجرا setup را خراب می‌کند یا نه.

## ورودی

```text
spread_points
spread_to_risk_ratio
spread_to_reward_ratio
raw_rr_like
effective_rr_after_spread
entry_type
symbol
scale
```

## خروجی

```text
execution_cost_class
execution_allowed
effective_rr_after_spread
```

حالت‌ها:

```text
EXEC_COST_OK
EXEC_COST_ACCEPTABLE
EXEC_COST_DEGRADES_OPTIONALITY
EXEC_COST_BLOCKS_TRADE
```

## الگوریتم‌ها

### 7.1 Rule Gate

اگر spread_to_risk خیلی زیاد باشد، block.

### 7.2 Stress-Test Model

مدل می‌سنجد edge تحت spreadهای مختلف پایدار است یا نه.

### 7.3 Execution Downgrade Model

به‌جای حذف کامل، بعضی setupها downgrade می‌شوند:

```text
ALLOW_STRUCTURALLY_BUT_BLOCK_EXECUTION
```

---

# 8. Cancel / Replace Policy Model

## هدف

مدیریت pending limit order.

## سؤال اصلی

```text
آیا order هنوز زنده است؟
یا باید cancel/replace شود؟
```

## ورودی

```text
extreme_state
anchor_node_validity
new_better_extreme_exists
y_phase_changed
destination_changed
invalidation_geometry_broken
fractal_context_changed
spread_changed
```

## خروجی

```text
KEEP
CANCEL
REPLACE
WAIT
```

## الگوریتم‌ها

### 8.1 Rule Policy Baseline

مثلاً:

```text
اگر Y-phase تغییر کرد، cancel.
اگر نود invalid شد، cancel.
اگر extreme بهتر ساخته شد، replace.
```

### 8.2 Offline Policy Learning

با backtest simulator بررسی می‌کنیم:

```text
اگر cancel می‌کردیم بهتر بود؟
اگر replace می‌کردیم بهتر بود؟
اگر نگه می‌داشتیم بهتر بود؟
```

### 8.3 Contextual Bandit / Policy Model

بعد از simulator و labels، می‌توان policy model ساخت.

اما قبل از simulator نباید رفت سراغ reinforcement.

---

# 9. Hedge Permission Model

## هدف

تشخیص اینکه دو سناریو می‌توانند همزمان execution داشته باشند یا نه.

## ورودی

```text
bullish_quality
bearish_quality
bullish_invalidation
bearish_invalidation
bullish_destination
bearish_destination
risk_overlap
spread_cost
fractal_conflict_type
scenario_balance_state
```

## خروجی

```text
NO_HEDGE
BOTH_WATCH_ONLY
DUAL_LIMIT_ALLOWED
HEDGE_ALLOWED
HEDGE_BLOCKED_RISK_OVERLAP
HEDGE_BLOCKED_EXECUTION_COST
```

## الگوریتم‌ها

### 9.1 Rule Gate

Hedge فقط وقتی مجاز است که هر دو طرف invalidation و destination روشن داشته باشند.

### 9.2 Risk Overlap Analyzer

تحلیل می‌کند که دو پوزیشن آیا فقط ریسک اضافه می‌کنند یا optionality می‌سازند.

### 9.3 Shadow Hedge Evaluator

اول در shadow تست می‌شود.

نباید مستقیم وارد paper/live شود.

---

# 10. Execution Template Selector

## هدف

انتخاب نوع اجرای مناسب.

## ورودی

```text
extreme_quality
scenario_rank
hook_rally_state
fractal_context
execution_cost
spread_to_risk
```

## خروجی

```text
LIMIT_AT_SELECTED_EXTREME
LIMIT_DEEPER_IN_EXTREME
WAIT_FOR_ZONE_TOUCH
WAIT_FOR_CHILD_TRIGGER
DO_NOT_CHASE
WATCH_ONLY
```

## الگوریتم‌ها

### 10.1 Template Baseline

چند template ساده تعریف می‌شود و تست می‌شود.

### 10.2 Template Ranker

AI انتخاب می‌کند کدام template در این context بهتر است.

---

# 11. ترتیب پیشنهادی ساخت

## مرحله 1

```text
Extreme Opportunity Dataset v1
```

بدون AI.

## مرحله 2

```text
Extreme Structural Labels v1
```

بدون AI.

## مرحله 3

```text
Rule-based Baseline Templates
```

برای مقایسه.

## مرحله 4

```text
Extreme Quality Model
```

اولین مدل AI.

## مرحله 5

```text
Dual Scenario Ranker
```

مدل دوم.

## مرحله 6

```text
Execution Cost Model
```

مدل سوم، چون stopها کوچک‌اند و spread حیاتی است.

## مرحله 7

```text
Cancel / Replace Policy
```

بعد از اینکه simulator داریم.

## مرحله 8

```text
F3 + Fractal Models
```

وقتی parent/current/child fields کامل شدند.

## مرحله 9

```text
Hedge Permission Model
```

فقط بعد از shadow evaluation.

---

# 12. کارهایی که می‌شود انجام داد

## 12.1 بدون AI

```text
تعریف اکستریم L2
ساخت dataset
ساخت labels
ساخت baseline
تست L2 مقابل L1/L3
تست cycle completion
تست spread
تست destination openness
```

## 12.2 با AI ساده اما مفید

```text
Extreme Quality Scoring
Scenario Ranking
Veto Model
Execution Cost Classifier
Template Selector
```

## 12.3 با AI پیشرفته‌تر

```text
F3 Terminal/Continuation Model
Fractal Context Model
Cancel/Replace Policy Learning
Hedge Permission Model
Optionality Exploiter
```

## 12.4 با Simulator

```text
offline policy learning
shadow decision comparison
paper execution evaluation
cancel/replace optimization
dual intent evaluation
```

---

# 13. ضد اورفیت

هیچ الگوریتمی بدون این‌ها قبول نیست:

```text
baseline comparison
negative controls
feature ablation
node-level ablation
cycle-completion sweep
spread stress
symbol/scale OOS
structural OOS
shadow evaluation
```

---

# 14. جمع‌بندی

برای تجربه اکستریم L2، الگوریتم‌های لازم این‌ها هستند:

```text
Deterministic Ontology Builder
Extreme Quality Model
Dual Scenario Ranker
Hook/Rally Ambiguity Model
F3 Terminal/Continuation Model
Fractal Context Model
Execution Cost Model
Cancel/Replace Policy Model
Hedge Permission Model
Execution Template Selector
```

اما ترتیب درست این است:

```text
اول dataset
بعد labels
بعد baseline
بعد AI
بعد simulator
بعد shadow
بعد paper
بعد live gate
```

AI قرار نیست اکستریم را از هیچ کشف کند.

امیر اکستریم را تعریف می‌کند.

AI یاد می‌گیرد کدام اکستریم‌ها ارزش اجرا دارند، کدام‌ها فریبنده‌اند، و با هرکدام باید چه execution policy انتخاب شود.

