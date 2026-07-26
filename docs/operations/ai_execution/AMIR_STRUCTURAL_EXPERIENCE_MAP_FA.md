# Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر

## وضعیت سند

این سند، تجربه‌های خام امیر درباره بازار، اکستریم‌ها، اف‌شماری، هوک/رالی، سناریوهای دوطرفه، فرکتال و اجرای لیمیت را تبدیل می‌کند به یک چارچوب قابل‌کدنویسی، قابل‌بک‌تست، قابل‌برچسب‌گذاری و قابل‌استفاده برای هوش مصنوعی.

این سند کد اجرایی نیست.

این سند مرجع مرحله‌های بعدی است:

```text
Experience Capture
→ Canonical State Packet
→ Structural Episode
→ Structural Labels
→ AI Algorithm Layers
→ ExecutionIntent
→ MT5 Backtest
→ Shadow / Paper / Live Gate
```

---

# 1. هسته تجربه امیر

تجربه اصلی امیر را می‌توان این‌گونه خلاصه کرد:

```text
بازار را نباید قطعی و تک‌سناریویی دید.
باید چند سناریوی همزمان ساخت.
برای buy دلیل آورد.
برای sell دلیل آورد.
برای Hook دلیل آورد.
برای Rally دلیل آورد.
در اکستریم‌های انتخاب‌شده دنبال optionality بود.
استاپ باید روی نود معتبر X-axis باشد.
ورود ترجیحاً limit در extreme است.
F3 یک terminal candidate است، اما با نگاه فرکتالی باید قضاوت شود.
اگر بعد از F3 continuation رخ دهد، احتمالاً parent scale هنوز انرژی ادامه دارد.
هزینه اجرا، مخصوصاً spread، باید داخل تصمیم باشد.
```

این نگاه یک سیستم پیش‌بینی خطی نیست.

این یک سیستم چندسناریویی است:

```text
Multi-Hypothesis
Fractal
Extreme-Based
Optionality-Driven
Execution-Aware
```

---

# 2. اصل اول — ورود در اکستریم‌ها

## تجربه خام

امیر می‌گوید:

```text
ورود در اکستریم‌ها می‌تواند reward خیلی خوبی بدهد.
جای stop loss هم معلوم است.
stop را روی نودی در محور X می‌گذاریم که بازار هنوز به آن نرسیده.
این باعث stopهای خیلی کوچک و rewardهای بزرگ می‌شود.
ورود باید تا حد ممکن limit باشد، نه chase.
```

## تفسیر ساختاری

Edge اصلی در وسط حرکت نیست.

Edge اصلی در selected extreme است.

یعنی ما دنبال جایی هستیم که:

```text
entry نزدیک extreme باشد
invalidation نزدیک باشد
destination باز باشد
risk کوچک باشد
reward بالقوه بزرگ باشد
```

این نگاه با breakout یا confirmation فرق دارد.

ما دنبال این نیستیم که بازار حرکت کند و بعد دنبال آن بدویم.

ما دنبال جایی هستیم که بازار اگر اشتباه کند، سریع و کوچک invalidate شود؛ و اگر درست باشد، payoff آزاد شود.

## تبدیل به hard rule

```text
هیچ entry بدون invalidation node معتبر نیست.
هیچ entry بدون destination معتبر نیست.
هیچ entry که invalidation آن مبهم باشد نباید به execution bridge برسد.
```

## تبدیل به feature

```text
selected_extreme_id
selected_extreme_kind
selected_extreme_price
selected_extreme_quality
selected_extreme_freshness
selected_extreme_depth
x_unreached_node_id
x_unreached_node_price
x_unreached_node_validity
distance_entry_to_invalidation
distance_entry_to_destination
rr_like
invalidation_tightness
destination_openness
extreme_to_current_distance
```

## تبدیل به label

```text
entry_touched
entry_missed
destination_before_invalidation
invalidation_before_destination
ambiguous_resolution
path_cleanliness_after_entry
optionality_realized_score
```

## تبدیل به execution policy

```text
LIMIT_AT_SELECTED_EXTREME
LIMIT_DEEPER_IN_EXTREME
DO_NOT_CHASE
CANCEL_IF_X_NODE_INVALIDATED
REPLACE_IF_BETTER_EXTREME_FORMS
BLOCK_IF_INVALIDATION_UNKNOWN
BLOCK_IF_DESTINATION_UNKNOWN
```

## نقش AI

AI اینجا نباید direction prediction کند.

AI باید بگوید:

```text
آیا این extreme واقعاً ارزش limit entry دارد؟
آیا این extreme فقط روی کاغذ قشنگ است؟
آیا invalidation خیلی شکننده است؟
آیا destination واقعاً باز است؟
آیا spread optionality را خراب می‌کند؟
```

---

# 3. اصل دوم — سناریوی Buy و Sell باید همزمان ساخته شود

## تجربه خام

امیر می‌گوید:

```text
در شمارش، باید ادله‌های buy را دید.
بعد باید ادله‌های sell را هم دید.
هر لحظه باید برای هر دو سناریو دلیل آورد.
حتی جاهایی ممکن است hedge شود و آن هم اوکی است.
```

## تفسیر ساختاری

سیستم نباید dogmatic باشد.

نباید فقط بگوید:

```text
BUY
```

یا:

```text
SELL
```

بلکه باید دو پرونده جدا بسازد:

```text
Bullish Scenario
Bearish Scenario
```

هر پرونده باید دلیل، entry، invalidation، destination و difficulty خودش را داشته باشد.

## Dual Scenario Ledger

خروجی پیشنهادی در مرحله‌های بعد:

```text
dual_scenario_ledger_v1.csv
```

## fieldهای لازم

```text
bullish_case_alive
bullish_case_reason_count
bullish_case_quality
bullish_entry_candidate
bullish_invalidation
bullish_destination
bullish_rr_like
bullish_fractal_support
bullish_execution_difficulty

bearish_case_alive
bearish_case_reason_count
bearish_case_quality
bearish_entry_candidate
bearish_invalidation
bearish_destination
bearish_rr_like
bearish_fractal_support
bearish_execution_difficulty

scenario_balance_state
scenario_conflict_state
scenario_dominance_state
dual_intent_permission_state
```

## حالت‌های خروجی

```text
LONG_ONLY
SHORT_ONLY
BOTH_WATCH
BOTH_LIMIT_ALLOWED
HEDGE_ALLOWED
NO_TRADE_AMBIGUOUS
```

## نقش AI

AI باید کمک کند:

```text
کدام سناریو قوی‌تر است؟
کدام سناریو باید veto شود؟
آیا هر دو سناریو زنده‌اند؟
آیا dual watch کافی است؟
آیا dual limit مجاز است؟
آیا hedge منطقی است یا فقط ابهام خطرناک است؟
```

---

# 4. اصل سوم — Hook و Rally هم باید دوحالته دیده شوند

## تجربه خام

امیر می‌گوید:

```text
فرض کنیم در Hook هستیم، چطور تحلیل می‌کردیم؟
فرض کنیم در Rally هستیم و F-count داریم، آن‌وقت چطور می‌دیدیم؟
حکم قطعی نمی‌شود داد.
چندحالته باید نگاه کرد.
انعطاف باید وجود داشته باشد.
```

## تفسیر ساختاری

سیستم نباید فقط یک state قطعی بدهد:

```text
market_state = Rally
```

بلکه باید دو interpretation همزمان بسازد:

```text
Hook Hypothesis
Rally Hypothesis
```

برای هرکدام باید entry، invalidation، destination، کیفیت، conflict و execution difficulty جدا ثبت شود.

## fieldهای لازم

```text
hook_hypothesis_alive
hook_hypothesis_quality
hook_entry_candidate
hook_invalidation
hook_destination
hook_reason_vector
hook_execution_policy

rally_hypothesis_alive
rally_hypothesis_quality
rally_f_count
rally_f_type
rally_entry_candidate
rally_invalidation
rally_destination
rally_reason_vector
rally_execution_policy

hook_rally_conflict_state
hook_rally_dominance_state
hook_rally_ambiguity_score
```

## نقش AI

AI نباید بگوید:

```text
قطعاً Hook است.
```

یا:

```text
قطعاً Rally است.
```

بلکه باید بگوید:

```text
Hook interpretation زنده است اما کیفیت آن متوسط است.
Rally interpretation زنده است و optionality بهتری دارد.
اما execution difficulty برای Rally بیشتر است.
```

AI اینجا مدیر uncertainty ساختاری است.

---

# 5. اصل چهارم — F3 یک terminal candidate است

## تجربه خام

امیر می‌گوید:

```text
F3 نکته خیلی مهمی دارد.
وقتی F3 دارد می‌زند، لزوماً اولین F خلاف آن کنسلش نمی‌کند.
F3 آخر روند است و تموم‌کننده روند.
اما اگر بعد از reverse دوباره ادامه بدهد، یعنی از تایم‌فریم‌های بالاتر انرژی ادامه دارد.
```

## تفسیر ساختاری

F3 نباید ساده‌لوحانه به‌عنوان پایان قطعی دیده شود.

تعریف درست:

```text
F3 = Terminal Candidate
```

نه:

```text
F3 = Guaranteed Reversal
```

یعنی F3 به ما هشدار می‌دهد که ساختار current scale ممکن است به انتها نزدیک شده باشد.

اما اگر بعد از تلاش برگشتی، قیمت دوباره در جهت قبلی ادامه دهد، این می‌تواند نشان دهد:

```text
parent scale هنوز destination باز دارد
parent scale هنوز invalid نشده
parent scale انرژی continuation دارد
current scale فقط pause یا pullback ساخته
```

## fieldهای لازم

```text
f_type
f_count
f3_terminal_candidate
f3_reversal_attempt_seen
f3_reversal_attempt_quality
f3_reversal_failed
f3_continuation_after_reversal
f3_terminal_confirmed
f3_terminal_rejected
f3_parent_support
f3_parent_conflict
f3_current_scale_exhaustion_state
f3_continuation_pressure_state
```

## labelهای لازم

```text
f3_destination_before_invalidation
f3_reversal_attempt_success
f3_reversal_attempt_failed
f3_continuation_after_reversal
f3_terminal_confirmed_by_structure
f3_rejected_by_parent_continuation
```

## نقش AI

AI باید یاد بگیرد:

```text
کدام F3ها واقعاً terminal بودند؟
کدام F3ها فقط pause بودند؟
چه چیزی باعث شد F3 ادامه بدهد؟
چه زمانی اولین F خلاف بعد از F3 فقط نویز است؟
چه زمانی F خلاف بعد از F3 واقعاً reversal را تأیید می‌کند؟
```

---

# 6. اصل پنجم — نگاه فرکتالی حیاتی است

## تجربه خام

امیر می‌گوید:

```text
وقتی F3 ریورس می‌دهد و دوباره ادامه می‌دهد، یعنی از تایم‌فریم‌های بالاتر انرژی ادامه دارد.
دید فرکتالی خیلی خیلی مهم است.
این چندحالته بودن را باید فرکتالی دید.
```

## تفسیر ساختاری

ما نباید نگاه فرکتالی را به زبان کلاسیک trend در تایم‌فریم بالاتر تعریف کنیم.

نگاه فرکتالی ما باید زبان خودمان را داشته باشد:

```text
parent scale phase
current scale phase
child scale phase
parent F-count
current F-count
child F-count
parent destination openness
parent invalidation state
current selected extreme quality
child activation quality
```

## سه سطح اصلی

```text
Parent Scale
Current Scale
Child Scale
```

## fieldهای لازم

```text
parent_phase_hypothesis
current_phase_hypothesis
child_phase_hypothesis

parent_f_count
current_f_count
child_f_count

parent_destination_open
parent_invalidation_intact
parent_continuation_energy
parent_terminal_pressure

current_selected_extreme_quality
current_x_invalidation_quality
current_destination_quality

child_activation_quality
child_micro_structure_alignment
child_entry_cleanliness

fractal_alignment_state
fractal_conflict_state
fractal_energy_continuation_state
fractal_terminal_pressure_state
```

## حالت‌های مهم

```text
PARENT_SUPPORTS_CURRENT
PARENT_CONFLICTS_CURRENT
PARENT_CONTINUATION_OVERRIDES_CURRENT_F3
CURRENT_F3_TERMINAL_WITH_PARENT_SUPPORT
CHILD_TRIGGER_ONLY
CHILD_NOISE
FRACTAL_AMBIGUOUS
```

## نقش AI

AI باید کمک کند بفهمیم:

```text
آیا current setup با parent هم‌راستاست؟
آیا current F3 واقعاً terminal است؟
آیا parent هنوز continuation pressure دارد؟
آیا child فقط trigger است یا نویز؟
آیا current setup داخل دیوار parent است؟
```

---

# 7. اصل ششم — ورود limit و هزینه اجرا

## تجربه خام

امیر می‌گوید:

```text
موقع ورود در اکستریم‌ها باید limit داشته باشیم.
spread هم باید حساب شود.
```

## تفسیر ساختاری

وقتی stop کوچک است، spread کوچک هم می‌تواند کل setup را خراب کند.

اگر risk_distance خیلی کوچک باشد، spread_to_risk_ratio حیاتی می‌شود.

یک setup ممکن است از نظر ساختاری عالی باشد، اما از نظر execution خراب باشد.

## fieldهای لازم

```text
spread_points
spread_price
risk_distance
reward_distance
spread_to_risk_ratio
spread_to_reward_ratio
effective_entry_price
effective_stop_distance
effective_rr_after_spread
execution_cost_class
```

## حالت‌های execution cost

```text
EXEC_COST_OK
EXEC_COST_ACCEPTABLE
EXEC_COST_DEGRADES_OPTIONALITY
EXEC_COST_BLOCKS_TRADE
```

## rule پیشنهادی

```text
اگر spread_to_risk_ratio از حد مجاز بیشتر باشد، setup باید downgrade یا block شود.
```

## نقش AI

AI باید بتواند بگوید:

```text
ساختار خوب است اما اجرای آن گران است.
ساختار متوسط است اما execution بسیار تمیز است.
این setup فقط در spread پایین مجاز است.
این setup برای limit خوب است اما برای market ممنوع است.
```

---

# 8. اصل هفتم — hedge یا dual intent باید رسمی شود

## تجربه خام

امیر می‌گوید:

```text
حتی جاهایی ممکن است hedge شود و آن هم اوکی است.
```

## تفسیر ساختاری

Hedge نباید یک تصمیم احساسی یا بی‌قاعده باشد.

باید تبدیل شود به state رسمی:

```text
DUAL_INTENT
```

یا:

```text
HEDGE_ALLOWED
```

اما فقط وقتی:

```text
هر دو سناریو X معتبر دارند
هر دو invalidation مشخص دارند
هر دو destination دارند
هر دو execution cost قابل قبول دارند
fractal conflict به‌جای رد کامل، dual optionality می‌سازد
```

## fieldهای لازم

```text
dual_intent_allowed
dual_intent_reason
long_intent_quality
short_intent_quality
long_short_correlation_context
dual_risk_overlap
dual_invalidation_overlap
hedge_execution_difficulty
```

## حالت‌ها

```text
NO_HEDGE
BOTH_WATCH_ONLY
DUAL_LIMIT_ALLOWED
HEDGE_ALLOWED
HEDGE_BLOCKED_RISK_OVERLAP
HEDGE_BLOCKED_EXECUTION_COST
HEDGE_BLOCKED_NO_CLEAR_INVALIDATION
```

## نقش AI

AI باید بفهمد:

```text
آیا هر دو طرف واقعاً opportunity هستند؟
یا فقط ambiguity خطرناک داریم؟
آیا hedge optionality ایجاد می‌کند؟
یا فقط هزینه و noise اضافه می‌کند؟
```

---

# 9. AI در این تجربه‌ها چه کاری انجام می‌دهد؟

AI در این پروژه predictor خام نیست.

AI باید این کارها را انجام دهد:

```text
سناریوها را زنده یا مرده تشخیص دهد
buy و sell را جداگانه rank کند
Hook و Rally را جداگانه rank کند
F3 terminal یا continuation را از context بفهمد
فرکتال parent/current/child را وزن دهد
اکستریم‌های خوب را از اکستریم‌های بد جدا کند
spread و execution difficulty را وارد تصمیم کند
limit / wait / cancel / replace / hedge را انتخاب کند
```

## خروجی‌های AI نباید order باشند

AI نباید بگوید:

```text
BUY 0.1 lot
SELL 0.2 lot
```

AI باید بگوید:

```text
ALLOW
VETO
DELAY
WATCH
LIMIT_AT_EXTREME
REPLACE_LIMIT
CANCEL
HEDGE_ALLOWED
```

و این خروجی باید تبدیل شود به:

```text
ExecutionIntent
```

---

# 10. مدل‌های AI پیشنهادی برای این تجربه‌ها

## 10.1 Extreme Quality Model

هدف:

```text
تشخیص کیفیت selected extreme برای limit entry
```

ورودی‌ها:

```text
selected_extreme_quality
x_unreached_node_validity
distance_to_invalidation
distance_to_destination
rr_like
spread_to_risk_ratio
fractal_alignment_state
```

خروجی:

```text
extreme_quality_score
ALLOW / VETO / DELAY
```

---

## 10.2 Dual Scenario Ranker

هدف:

```text
رتبه‌بندی buy و sell همزمان
```

خروجی:

```text
bullish_rank_score
bearish_rank_score
scenario_balance_state
```

---

## 10.3 Hook/Rally Ambiguity Model

هدف:

```text
مدیریت دو تفسیر Hook و Rally
```

خروجی:

```text
hook_quality_score
rally_quality_score
hook_rally_dominance_state
```

---

## 10.4 F3 Terminal / Continuation Model

هدف:

```text
تشخیص اینکه F3 واقعاً terminal است یا parent continuation آن را override می‌کند
```

خروجی:

```text
f3_terminal_probability_like
f3_continuation_pressure_score
f3_parent_override_state
```

---

## 10.5 Fractal Context Model

هدف:

```text
وزن دادن به parent/current/child alignment و conflict
```

خروجی:

```text
fractal_alignment_score
fractal_conflict_class
parent_energy_state
```

---

## 10.6 Execution Cost Model

هدف:

```text
تشخیص اینکه spread و هزینه اجرا setup را خراب می‌کند یا نه
```

خروجی:

```text
execution_cost_class
effective_rr_after_spread
execution_allowed
```

---

## 10.7 Cancel / Replace Policy Model

هدف:

```text
مدیریت pending limit order
```

خروجی:

```text
KEEP
CANCEL
REPLACE
WAIT
```

---

## 10.8 Hedge Permission Model

هدف:

```text
تشخیص اینکه dual scenario می‌تواند hedge/dual intent شود یا فقط ambiguity خطرناک است
```

خروجی:

```text
NO_HEDGE
BOTH_WATCH_ONLY
DUAL_LIMIT_ALLOWED
HEDGE_ALLOWED
```

---

# 11. تست‌های ضد اورفیت مخصوص این تجربه‌ها

## برای اکستریم‌ها

```text
random extreme control
nearest node control
random node invalidation control
spread stress test
destination shuffle
```

## برای dual scenario

```text
direction flip test
bull/sell label shuffle
single-side-only baseline
both-side-random baseline
```

## برای Hook/Rally

```text
hook/rally swapped labels
ambiguous-state-only test
dominant-state-only test
```

## برای F3

```text
F3-only baseline
F1/F2/F3 shuffle
parent-scale removed ablation
child-scale removed ablation
terminal-label shuffle
```

## برای فرکتال

```text
parent removed
child removed
current only
fractal alignment shuffled
parent continuation label shuffled
```

## برای execution cost

```text
zero spread baseline
high spread stress
random spread perturbation
effective RR vs raw RR comparison
```

## برای hedge

```text
hedge allowed vs no hedge
dual watch vs dual limit
random dual scenario baseline
risk overlap stress
```

---

# 12. سؤال‌های باز برای شفاف‌سازی

این بخش باید بعداً با جواب‌های امیر کامل شود.

## اکستریم و X-axis

```text
اکستریم دقیقاً کدام نود یا زون است؟
اگر چند اکستریم باشد، کدام انتخاب شود؟
نود stop دقیقاً چه ویژگی دارد؟
نود X که بازار هنوز به آن نرسیده یعنی دقیقاً چه؟
```

## سایکل‌های ۹۰ درصد

```text
منظور از سایکل‌های ۹۰ درصد چیست؟
یعنی چرخه تقریباً کامل شده؟
یعنی بازار نزدیک مقصد است؟
یعنی اکستریم در انتهای چرخه است؟
یعنی stop خیلی کوچک و reward خیلی باز است؟
```

## Buy/Sell

```text
حداقل دلیل برای زنده بودن bullish scenario چیست؟
حداقل دلیل برای bearish scenario چیست؟
چه زمانی هر دو valid هستند؟
چه زمانی باید یکی veto شود؟
چه زمانی dual intent مجاز است؟
```

## Hook/Rally

```text
Hook چه زمانی زنده است؟
Hook چه زمانی می‌میرد؟
Rally چه زمانی زنده است؟
Rally چه زمانی تمام می‌شود؟
اگر هر دو interpretation زنده باشند، execution چه کند؟
```

## F3

```text
هر F3 terminal candidate است یا فقط F3 خاص؟
چه چیزی F3 را terminal confirmed می‌کند؟
چه چیزی F3 را continuation می‌کند؟
چرا اولین F خلاف لزوماً cancel نمی‌کند؟
```

## فرکتال

```text
چند scale باید بررسی شود؟
parent scale چه زمانی انرژی ادامه دارد؟
اگر current خلاف parent باشد چه کنیم؟
اگر child خلاف current باشد چه کنیم؟
```

## execution

```text
حداکثر spread_to_risk_ratio چقدر است؟
market entry کجا مجاز است؟
pending order چه زمانی cancel شود؟
pending order چه زمانی replace شود؟
چه زمانی hedge واقعاً مجاز است؟
```

---

# 13. نتیجه نهایی

تجربه‌های امیر سیستم را به این سمت می‌برند:

```text
چند سناریوی همزمان
چند interpretation همزمان
ورود در extreme
stop روی X node
destination باز
F3 به‌عنوان terminal candidate
فرکتال به‌عنوان داور continuation یا termination
spread-aware execution
limit-first execution
AI به‌عنوان ranker / veto / router / execution policy selector
```

این دقیقاً پایه مناسب برای AI غیرکلاسیک است.

AI قرار نیست الگوی خام بسازد.

AI قرار است داخل جهان امیر، سناریوها را وزن دهد، فرصت‌ها را رتبه‌بندی کند، setupهای فریبنده را حذف کند و execution را هوشمندتر کند.

