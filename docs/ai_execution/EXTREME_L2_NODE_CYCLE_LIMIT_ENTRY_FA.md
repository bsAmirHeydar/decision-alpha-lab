# Extreme L2 Node Cycle Limit Entry — تعریف رسمی اکستریم، نود L2 و ورود لیمیت

## وضعیت سند

این سند تعریف رسمی تجربه‌ی امیر درباره ورود در اکستریم‌هاست.

موضوع اصلی:

```text
اکستریم = ناحیه‌ی نزدیک نود نخورده، پیش‌فرضاً L2،
در حوالی کامل‌شدن چرخه،
با ورود limit خلاف جهت حرکت فعلی،
و stop پشت همان نود.
```

این سند کد اجرایی نیست.

این سند پایه‌ی مرحله‌های بعدی است:

```text
Canonical State Packet
Structural Episode Builder
Extreme Opportunity Label Engine
AI Extreme Quality Model
ExecutionIntent
MT5 Backtest Simulator
```

---

# 1. تصویر مرجع

در تصویر نمونه، ناحیه قرمز حوالی نود `ND L2 #4` به‌عنوان اکستریم مشخص شده است.

```text
docs/ai_execution/assets/extreme_l2_node_example.png
```

برداشت رسمی از تصویر:

```text
قیمت به ناحیه نزدیک نود L2 نخورده رسیده است.
آن ناحیه اکستریم محسوب می‌شود.
ورود ایده‌آل، نزدیک همان ناحیه و خلاف جهت حرکت فعلی است.
استاپ پشت همان نود قرار می‌گیرد.
بازار از آن ناحیه ریورس کرده است.
```

---

# 2. تعریف پایه

## تعریف انسانی

امیر می‌گوید:

```text
اکستریم یعنی ورود در نزدیکی نودی که زده نشده.
در جای درستش و با توجه به سناریوها، stop پشت آن نود می‌رود.
پیش‌فرض نود مورد بررسی برای اکستریم L2 است.
قیمت وقتی به نزدیکی مثلاً 90 درصد سایکل آن نود می‌رسد، آن ناحیه می‌شود اکستریم.
استاپ پشت نود است.
ورود نزدیک همان ناحیه و خلاف جهت حرکت فعلی است.
```

## تعریف رسمی

```text
Extreme Opportunity =
Scenario-valid approach toward an unreached L2 node,
near structural cycle completion,
where a contrarian limit entry can be placed near the node,
with stop behind the node,
and destination open enough to justify optionality.
```

به فارسی:

```text
فرصت اکستریم =
رسیدن قیمت، در سناریوی معتبر، به نزدیکی نود L2 نخورده،
در حوالی تکمیل چرخه،
برای ورود لیمیت خلاف جهت حرکت فعلی،
با استاپ پشت همان نود،
و مقصدی که به اندازه کافی باز باشد.
```

---

# 3. اکستریم چیست و چه چیزی نیست؟

## اکستریم هست

```text
ناحیه نزدیک نود نخورده
ناحیه‌ای با invalidation روشن
ناحیه‌ای مناسب برای limit
ناحیه‌ای با stop کوچک
ناحیه‌ای با destination بالقوه باز
ناحیه‌ای وابسته به سناریوی buy/sell و Hook/Rally
```

## اکستریم نیست

```text
هر high/low خام
هر حمایت/مقاومت کلاسیک
هر زون دلخواه
هر برگشت تصادفی
هر ورود بعد از confirmation
هر chase بعد از حرکت
```

---

# 4. اجزای اکستریم

## 4.1 Scenario Context

اکستریم بدون سناریو معنا ندارد.

قبل از اینکه بگوییم یک ناحیه اکستریم است، باید بدانیم:

```text
در سناریوی bullish، این نود چه نقشی دارد؟
در سناریوی bearish، این نود چه نقشی دارد؟
اگر Hook باشد، این نود چه معنایی دارد؟
اگر Rally باشد، این نود چه معنایی دارد؟
در parent scale این ناحیه حمایت می‌شود یا conflict دارد؟
```

پس اکستریم همیشه باید داخل چند پرونده بررسی شود:

```text
Bullish Case
Bearish Case
Hook Hypothesis
Rally Hypothesis
Parent Scale Context
Current Scale Context
Child Scale Context
```

---

## 4.2 Anchor Node

نود مرجع اکستریم:

```text
extreme_anchor_node
```

پیش‌فرض:

```text
node_level = L2
```

ویژگی‌ها:

```text
نود باید هنوز کاملاً زده نشده باشد.
نود باید در محور X قابل شناسایی باشد.
نود باید جای استاپ را مشخص کند.
نود باید نسبت به سناریوی فعلی معنا داشته باشد.
```

fieldهای لازم:

```text
extreme_anchor_node_id
extreme_anchor_node_level
extreme_anchor_node_price
extreme_anchor_node_index
extreme_anchor_node_unreached
extreme_anchor_node_role
extreme_anchor_node_validity
```

---

## 4.3 Extreme Zone

اکستریم خود نود نیست.

اکستریم ناحیه نزدیک نود است.

```text
Extreme Zone = proximity band around the unreached anchor node
```

fieldهای لازم:

```text
extreme_zone_id
extreme_zone_upper
extreme_zone_lower
extreme_zone_mid
extreme_zone_width
extreme_zone_relation_to_node
price_inside_extreme_zone
```

ابهام باز:

```text
عرض زون باید ثابت باشد؟
وابسته به فاصله نود تا current price باشد؟
وابسته به spread باشد؟
وابسته به ساختار X باشد؟
وابسته به scale باشد؟
```

---

## 4.4 Cycle Completion

تعبیر امیر:

```text
قیمت به نزدیکی مثلاً 90 درصد سایکل یک نود رسیده است.
```

برداشت رسمی فعلی:

```text
cycle_completion_ratio ≈ degree of structural approach from cycle origin toward unreached node
```

نسخه اولیه field:

```text
cycle_origin_price
cycle_anchor_node_price
current_price
cycle_completion_ratio
cycle_near_completion
```

برای bullish approach:

```text
cycle_completion_ratio =
(current_price - cycle_origin_price) / (anchor_node_price - cycle_origin_price)
```

برای bearish approach:

```text
cycle_completion_ratio =
(cycle_origin_price - current_price) / (cycle_origin_price - anchor_node_price)
```

اما این فقط نسخه‌ی عددی اولیه است.

نسخه دقیق‌تر باید بعداً با منطق ساختاری امیر تنظیم شود.

حالت‌های پیشنهادی:

```text
CYCLE_EARLY
CYCLE_MID
CYCLE_LATE
CYCLE_EXTREME_APPROACH
CYCLE_AT_NODE
CYCLE_NODE_BROKEN
```

پیشنهاد اولیه:

```text
CYCLE_EXTREME_APPROACH وقتی cycle_completion_ratio حدوداً بین 0.85 تا 1.00 باشد.
```

اما عدد 0.90 نباید کورکورانه hardcode شود تا وقتی تست نشده است.

---

## 4.5 Entry Logic

ورود مطلوب:

```text
contrarian limit entry near extreme zone
```

یعنی:

```text
قیمت در حال حرکت به سمت نود است.
ما در نزدیکی نود، خلاف جهت حرکت جاری limit می‌گذاریم.
```

حالت‌ها:

```text
LIMIT_AT_EXTREME_ZONE_EDGE
LIMIT_AT_EXTREME_ZONE_MID
LIMIT_DEEPER_BEHIND_ZONE
WAIT_FOR_ZONE_TOUCH
NO_CHASE
```

fieldهای لازم:

```text
extreme_entry_price
extreme_entry_direction
entry_relation_to_zone
entry_relation_to_node
entry_limit_allowed
entry_market_allowed
entry_chase_forbidden
```

اصل پیشنهادی:

```text
market entry پیش‌فرضاً مجاز نیست.
limit entry پیش‌فرض اصلی است.
chase ممنوع است مگر سند جداگانه خلافش را ثابت کند.
```

---

## 4.6 Stop Logic

استاپ:

```text
behind anchor node
```

fieldهای لازم:

```text
stop_anchor_node_id
stop_anchor_node_price
stop_side
stop_buffer_points
stop_price
stop_distance
stop_distance_after_spread
```

ابهام باز:

```text
پشت نود دقیقاً چند point؟
پشت زون؟
با buffer ثابت؟
با buffer ساختاری؟
با spread-adjustment؟
```

نسخه اولیه:

```text
stop_price = behind node + structural/spread buffer
```

---

## 4.7 Destination Logic

اکستریم بدون destination باز ارزشی ندارد.

fieldهای لازم:

```text
destination_id
destination_price
destination_kind
destination_open
destination_distance
destination_quality
destination_blocked_by_parent
destination_changed
```

اگر destination بسته باشد:

```text
EXTREME_STRUCTURALLY_VALID_BUT_NO_DESTINATION
```

اگر destination باز باشد:

```text
EXTREME_OPTIONALITY_AVAILABLE
```

---

## 4.8 Spread-Aware Optionality

چون stopها کوچک‌اند، spread حیاتی است.

fieldهای لازم:

```text
spread_points
spread_price
risk_distance_raw
risk_distance_effective
reward_distance_raw
reward_distance_effective
raw_rr_like
effective_rr_after_spread
spread_to_risk_ratio
spread_to_reward_ratio
```

حالت‌های execution cost:

```text
EXEC_COST_OK
EXEC_COST_ACCEPTABLE
EXEC_COST_DEGRADES_OPTIONALITY
EXEC_COST_BLOCKS_TRADE
```

اصل:

```text
اگر spread_to_risk_ratio زیاد باشد، حتی اکستریم خوب هم ممکن است execution-invalid شود.
```

---

# 5. وضعیت‌های اکستریم

پیشنهاد state machine:

```text
EXTREME_NOT_AVAILABLE
EXTREME_CANDIDATE
EXTREME_APPROACHING
EXTREME_ZONE_TOUCHED
EXTREME_LIMIT_PLACED
EXTREME_FILLED
EXTREME_REVERSED
EXTREME_INVALIDATED
EXTREME_MISSED
EXTREME_SUPERSEDED
EXTREME_BLOCKED_BY_SPREAD
EXTREME_BLOCKED_BY_SCENARIO
EXTREME_BLOCKED_BY_FRACTAL
```

---

# 6. labelهای لازم

برای اینکه AI یاد بگیرد، باید outcomeهای ساختاری بسازیم.

## 6.1 Activation Labels

```text
entry_touched
entry_filled
entry_missed
node_touched
node_broken
```

## 6.2 Resolution Labels

```text
destination_before_invalidation
invalidation_before_destination
reversal_from_extreme
continuation_through_node
ambiguous_resolution
```

## 6.3 Path Labels

```text
path_cleanliness_after_entry
max_adverse_excursion_r
max_favorable_excursion_r
dirty_reversal
clean_reversal
```

## 6.4 Execution Labels

```text
effective_rr_after_spread
spread_destroyed_optionality
limit_fill_quality
market_entry_would_be_bad
cancel_would_have_helped
replace_would_have_helped
```

---

# 7. تست‌های ضد اورفیت مخصوص اکستریم

هر الگوریتمی که روی اکستریم train می‌شود، باید این تست‌ها را پاس کند.

## 7.1 Random Extreme Control

اکستریم واقعی را با extremeهای تصادفی مقایسه می‌کنیم.

اگر مدل روی random extreme هم خوب باشد، garbage است.

## 7.2 Random Node Control

نود L2 واقعی را با نودهای تصادفی یا نودهای بی‌ربط مقایسه می‌کنیم.

## 7.3 Node Level Ablation

بررسی می‌کنیم:

```text
L1 only
L2 only
L3 only
All nodes
No node level
```

اگر L2 واقعاً پایه خوبی است، باید نسبت به کنترل‌ها معنی‌دار باشد.

## 7.4 Cycle Completion Sweep

نسبت‌های مختلف را تست می‌کنیم:

```text
70%
75%
80%
85%
90%
95%
100%
```

هدف این نیست که عدد 90 را curve-fit کنیم.

هدف این است بفهمیم آیا محدوده‌ی late-cycle واقعاً بهتر است یا نه.

## 7.5 Spread Stress Test

```text
zero spread
normal spread
2x spread
3x spread
high spread
```

اگر edge فقط در spread صفر وجود دارد، قابل اجرا نیست.

## 7.6 Destination Shuffle

destination واقعی را shuffle می‌کنیم.

اگر مدل هنوز خوب بماند، احتمالاً دارد leakage یا الگوی فیک یاد می‌گیرد.

---

# 8. خروجی‌های لازم در آینده

## 8.1 Extreme Opportunity Dataset

```text
extreme_opportunity_dataset_v1.csv
```

ستون‌های اصلی:

```text
episode_id
scenario_id
anchor_node_id
anchor_node_level
anchor_node_unreached
cycle_completion_ratio
extreme_zone_touched
entry_price
stop_price
destination_price
raw_rr_like
effective_rr_after_spread
fractal_context
hook_rally_context
f_count_context
extreme_state
```

## 8.2 Extreme Labels

```text
extreme_opportunity_labels_v1.csv
```

ستون‌های اصلی:

```text
episode_id
entry_filled
destination_before_invalidation
invalidation_before_destination
reversal_from_extreme
node_broken
path_cleanliness_score
optionality_realized_score
spread_destroyed_optionality
```

## 8.3 Extreme AI Signals

```text
extreme_ai_signal_v1.csv
```

ستون‌های اصلی:

```text
episode_id
model_id
extreme_quality_score
allow_veto_delay
entry_template_id
cancel_policy_id
replace_policy_id
reason_vector
```

---

# 9. سؤال‌های باز برای امیر

این‌ها باید در نسخه بعدی سند تکمیل شوند.

## 9.1 نزدیکی به نود

```text
نزدیکی به نود دقیقاً یعنی چه؟
یک فاصله ثابت؟
درصدی از حرکت؟
داخل زون اطراف نود؟
وابسته به spread؟
وابسته به scale؟
```

## 9.2 90 درصد سایکل

```text
90 درصد یعنی نسبت عددی مسیر از origin تا node؟
یا مفهوم ساختاری late-cycle؟
یا شهودی است؟
```

## 9.3 stop پشت نود

```text
پشت نود یعنی چند point؟
پشت wick/zone؟
با spread؟
با buffer ثابت؟
با buffer ساختاری؟
```

## 9.4 L2

```text
L2 همیشه default است؟
یا L2 فقط پیش‌فرض اولیه است؟
آیا L1/L3 هم در contextهای خاص extreme می‌سازند؟
```

## 9.5 Entry trigger

```text
limit صرفاً روی رسیدن به zone؟
یا نیاز به نشانه‌ی ریورس؟
آیا confirmation ممنوع است؟
آیا trigger child-scale مجاز است؟
```

## 9.6 Node penetration

```text
اگر نود کمی زده شد ولی stop نخورد، هنوز معتبر است؟
یا هر لمس نود یعنی فرصت تمام شده؟
```

---

# 10. نتیجه

تعریف رسمی فعلی:

```text
Extreme L2 Node Opportunity =
رسیدن قیمت به ناحیه نزدیک نود L2 نخورده،
در حوالی تکمیل چرخه،
در context سناریویی معتبر،
برای ورود limit خلاف حرکت جاری،
با stop پشت نود،
با destination باز،
و با spread قابل قبول.
```

این تعریف باید پایه‌ی اولین dataset جدی AI و اولین execution simulator حرفه‌ای باشد.

