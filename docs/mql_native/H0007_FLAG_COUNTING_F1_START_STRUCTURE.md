# H0007 — Flag Counting / F1 Start Structure

> Status: design lock, topology-only.  
> Version: v0.2 — nested `R12` rule added and expanded.  
> Layer: structural grammar on top of the M0001 final-only known-time node stream.  
> Scope: define and audit **F1 only**. F2 and F3 are intentionally out of scope until F1 is mechanically stable.

---

## 0. Why this document exists

The purpose of this README is to turn the visual idea of **F1** into a mechanical object.

F1 must not remain a drawing. It must become something that the code can count, draw, invalidate, confirm, export, and later compare against random baselines.

This document is therefore not a trading strategy. It is a **structural counting contract**.

The detector must answer one narrow question first:

```text
Can a protected-waist F1 be detected from structural nodes, in known-time order, without future leakage, and drawn on the chart exactly as intended?
```

Only after that can H0007 ask alpha questions such as forward MFE, MAE, path cleanliness, directional memory, optionality, or execution quality.

---

## 1. Core thesis

The working thesis is:

```text
The market can be parsed as a chain of flags.
```

But this project does not accept vague chart-pattern language. A flag must be reduced to:

```text
known-time nodes
ordered structural states
protected invalidation level
internal count
internal trigger
main confirmation
full event record
visual audit
random comparison later
```

H0007 starts with the first object in that grammar:

```text
F1 = first/start flag structure
```

F1 is the start structure of a movement. It often appears after two hooks, or after an opposite violent move, or after a market area where the previous side is no longer dominant. These contexts may be logged later, but they are **not required filters** in the base definition.

---

## 2. Reference sketches

Bullish F1 sketch:

![Bullish F1 sketch](../../assets/H0007/f1.png)

Hook-hook-to-F1 context sketch:

![Hook hook F1 sketch](../../assets/H0007/flag-hook-hook-f1.png)

The drawings are visual references, not the algorithm. The algorithm is the topology and state machine below.

---

## 3. Critical corrections locked in v0.2

There are two critical rules that must not be lost.

### 3.1 `R12` break is not final confirmation

For bullish F1:

```text
Break above R12 = internal trigger / armed state
Break above H2  = final F1 confirmation
```

For bearish F1:

```text
Break below R12 = internal trigger / armed state
Break below L2  = final F1 confirmation
```

So F1 is not confirmed just because the roof/floor between count node 1 and count node 2 breaks.

### 3.2 `R12` must stay inside the main second extreme

This is the new precision rule.

For bullish F1:

```text
R12 must be lower than H2.
```

For bearish F1:

```text
R12 must be higher than L2.
```

This means `R12` is an **internal reaction level**, not the main second roof/floor itself.

If the supposed `R12` reaches or breaks the main second extreme before a valid `N2` exists, the candidate is not a clean F1. It is direct continuation or a different structure, and the F1 candidate must be rejected or reset.

---

## 4. Canonical naming

This README uses the following names.

### 4.1 Bullish F1 names

| Symbol | Name | Role |
|---|---|---|
| `H1` | first roof | first structural high before the protected waist |
| `W` | waist | protected structural low after `H1`; red invalidation line |
| `H2` | main second roof | structural high after `W` that breaks `H1`; final confirmation level later |
| `N1` | count node 1 | first internal structural low after `H2` |
| `R12` | internal roof | structural high between `N1` and `N2`; must be below `H2` |
| `N2` | count node 2 | second internal low, below `N1`, but above `W` |
| `T12` | internal trigger | first break above `R12` after `N2` |
| `CONF` | confirmation | first break above `H2` after the internal trigger |

### 4.2 Bearish F1 names

| Symbol | Name | Role |
|---|---|---|
| `L1` | first floor | first structural low before the protected waist |
| `W` | waist | protected structural high after `L1`; red invalidation line |
| `L2` | main second floor | structural low after `W` that breaks `L1`; final confirmation level later |
| `N1` | count node 1 | first internal structural high after `L2` |
| `R12` | internal floor | structural low between `N1` and `N2`; must be above `L2` |
| `N2` | count node 2 | second internal high, above `N1`, but below `W` |
| `T12` | internal trigger | first break below `R12` after `N2` |
| `CONF` | confirmation | first break below `L2` after the internal trigger |

`R12` means reaction level between count node `1` and count node `2`.

In bullish mode it is a roof.  
In bearish mode it is a floor.

---

## 5. F1 is not a trade

F1 is only a structural event.

The base detector must not output:

```text
entry
stop-loss
take-profit
profit factor
win rate
R multiple
execution recommendation
```

The base detector outputs only:

```text
candidate states
confirmed F1 events
invalidations
ambiguities
structural measurements
chart objects
raw records
```

Trading logic belongs to a later module after F1 is visually and statistically audited.

---

## 6. Source contract: known-time nodes only

F1 must be built on the same causality discipline as the rest of Decision Alpha Lab.

Required source:

```text
M0001 final-only structural node stream
```

Required timing contract:

```text
A pivot can be drawn at its pivot candle,
but the algorithm can only use it after its reveal/known time.
```

For a pivot with scale `L`:

```text
pivot_index = i
known_index = i + L
```

The chart may anchor the label at `i`, but the state machine must not react before `i + L`.

This is non-negotiable. F1 must not use future-known pivots.

---

## 7. Scale `L` contract

F1 is counted per node scale.

```text
L_min = 2
L_max = configurable
```

The first implementation must run separate passes:

```text
L = 2
L = 3
L = 4
...
L = L_max
```

A single F1 candidate cannot change `L` while forming.

Base rule:

```text
one F1 = one symbol + one timeframe + one direction + one L
```

Later, cross-scale confluence can be studied:

```text
same F1 area appears across nearby L values => possible structural strength
```

But cross-L merging must not happen inside the raw detector.

---

## 8. Bullish F1: strict topology

A bullish F1 candidate must form this known-time sequence:

```text
H1 -> W -> H2 -> N1 -> R12 -> N2 -> T12 -> CONF
```

The required inequalities are:

```text
H2  > H1
W   < H1
N1  > W
R12 > N1
R12 < H2
N2  < N1
N2  > W
T12 breaks above R12
CONF breaks above H2
```

The most important nested condition is:

```text
R12 < H2
```

That condition means the roof between `1` and `2` is still inside the F1 body. It is not allowed to be the main second roof, and it is not allowed to exceed the main second roof.

### 8.1 Bullish structural meaning

The bullish structure says:

```text
1. Market creates H1.
2. Market pulls back and creates W.
3. Market breaks H1 and creates H2.
4. Market pulls back and creates N1.
5. Market reacts upward, but only internally, creating R12 below H2.
6. Market pulls back again and creates N2 below N1 but above W.
7. Market breaks R12, proving local recovery from the 1-2 correction.
8. Market then breaks H2, proving the full F1 continuation/confirmation.
```

### 8.2 Bullish invalidation

From the moment `W` exists until final confirmation:

```text
W must not break.
```

Base wick-strict rule:

```text
if bar.low < W.price - epsilon:
    invalidate bullish candidate
```

### 8.3 Bullish internal trigger vs final confirmation

After `N2`, there are two levels above price:

```text
R12 = internal roof
H2  = main second roof
```

They have different meanings:

```text
Break R12 => the 1-2 correction is locally reclaimed.
Break H2  => the whole F1 is confirmed.
```

Therefore:

```text
R12 break alone is not enough.
H2 break is mandatory.
```

### 8.4 Bullish rejection cases

Reject or reset the bullish candidate if:

```text
W breaks before confirmation.
N2 does not go below N1.
N2 breaks or touches below W in strict mode.
R12 is not below H2.
H2 is broken again before a valid N2 exists.
The structure needs a different L halfway through.
Known-time order is violated.
```

If a structural high after `N1` is `>= H2`, it cannot be accepted as `R12`. In the strict base detector, this is:

```text
continuation_without_valid_1_2_count
```

and the candidate should be rejected/reset.

---

## 9. Bearish F1: strict topology

A bearish F1 candidate must form this known-time sequence:

```text
L1 -> W -> L2 -> N1 -> R12 -> N2 -> T12 -> CONF
```

The required inequalities are:

```text
L2  < L1
W   > L1
N1  < W
R12 < N1
R12 > L2
N2  > N1
N2  < W
T12 breaks below R12
CONF breaks below L2
```

The most important nested condition is:

```text
R12 > L2
```

That condition means the floor between `1` and `2` is still inside the F1 body. It is not allowed to be the main second floor, and it is not allowed to exceed the main second floor downward.

### 9.1 Bearish structural meaning

The bearish structure says:

```text
1. Market creates L1.
2. Market pulls back upward and creates W.
3. Market breaks L1 and creates L2.
4. Market pulls back upward and creates N1.
5. Market reacts downward, but only internally, creating R12 above L2.
6. Market pulls back upward again and creates N2 above N1 but below W.
7. Market breaks R12, proving local recovery from the 1-2 correction.
8. Market then breaks L2, proving the full F1 continuation/confirmation.
```

### 9.2 Bearish invalidation

From the moment `W` exists until final confirmation:

```text
W must not break.
```

Base wick-strict rule:

```text
if bar.high > W.price + epsilon:
    invalidate bearish candidate
```

### 9.3 Bearish internal trigger vs final confirmation

After `N2`, there are two levels below price:

```text
R12 = internal floor
L2  = main second floor
```

They have different meanings:

```text
Break R12 => the 1-2 correction is locally reclaimed.
Break L2  => the whole F1 is confirmed.
```

Therefore:

```text
R12 break alone is not enough.
L2 break is mandatory.
```

### 9.4 Bearish rejection cases

Reject or reset the bearish candidate if:

```text
W breaks before confirmation.
N2 does not go above N1.
N2 breaks or touches above W in strict mode.
R12 is not above L2.
L2 is broken again before a valid N2 exists.
The structure needs a different L halfway through.
Known-time order is violated.
```

If a structural low after `N1` is `<= L2`, it cannot be accepted as `R12`. In the strict base detector, this is:

```text
continuation_without_valid_1_2_count
```

and the candidate should be rejected/reset.

---

## 10. Equality, epsilon, and strictness

The base detector should be strict, but implementation needs explicit equality rules.

### 10.1 Base strict inequalities

Bullish:

```text
H2.price  > H1.price + epsilon
R12.price < H2.price - epsilon
N2.price  < N1.price - epsilon
N2.price  > W.price  + epsilon
```

Bearish:

```text
L2.price  < L1.price - epsilon
R12.price > L2.price + epsilon
N2.price  > N1.price + epsilon
N2.price  < W.price  - epsilon
```

If equality happens within epsilon, the event should be marked as:

```text
borderline_epsilon_case
```

and excluded from the clean base sample unless a specific tolerance mode includes it.

### 10.2 Base mode

```text
break_mode = wick_strict
epsilon = 0 by default
```

Later stability grid:

```text
epsilon = 0
epsilon = 1 * point
epsilon = 1 * spread
epsilon = 0.05 * ATR
epsilon = 0.10 * ATR
```

No claim is robust if it only works under one fragile epsilon setting.

---

## 11. Break definitions

### 11.1 Bullish break definitions

```text
bull_break(level, bar):
    return bar.high > level + epsilon

bull_waist_broken(W, bar):
    return bar.low < W.price - epsilon
```

Bullish internal trigger:

```text
bar.high > R12.price + epsilon
```

Bullish final confirmation:

```text
bar.high > H2.price + epsilon
```

### 11.2 Bearish break definitions

```text
bear_break(level, bar):
    return bar.low < level - epsilon

bear_waist_broken(W, bar):
    return bar.high > W.price + epsilon
```

Bearish internal trigger:

```text
bar.low < R12.price - epsilon
```

Bearish final confirmation:

```text
bar.low < L2.price - epsilon
```

---

## 12. Same-candle ambiguity

Historical OHLC does not always reveal intrabar order.

### 12.1 Waist and confirmation on the same candle

Bullish ambiguity:

```text
same candle:
    high > H2
    low  < W
```

Bearish ambiguity:

```text
same candle:
    low  < L2
    high > W
```

Default rule:

```text
mark ambiguous_same_bar
exclude from clean confirmed sample
```

Do not assume the favorable path.

### 12.2 R12 and H2 on the same candle

Bullish:

```text
same candle after valid N2:
    high > R12
    high > H2
    low does not break W
```

This can be logged as:

```text
same_bar_T12_CONF = true
```

Because any continuous move above `H2` necessarily crossed `R12` first. But if the waist also breaks on that candle, it becomes ambiguous and should not be part of the clean sample.

Bearish mirror applies.

---

## 13. Open count logic

F1 is not born all at once. It has count states.

Bullish:

```text
After H2 and N1:
    open_count = 1

After R12 and valid N2:
    open_count = 2

After break above R12:
    state = armed

After break above H2:
    state = confirmed_F1
```

Bearish:

```text
After L2 and N1:
    open_count = 1

After R12 and valid N2:
    open_count = 2

After break below R12:
    state = armed

After break below L2:
    state = confirmed_F1
```

The visual chart must show open count `1` and `2` even before confirmation in debug mode.

---

## 14. Bullish state machine

```text
STATE_IDLE
    wait for structural high H1

STATE_HAVE_H1
    wait for structural low W after H1
    W becomes protected waist
    if a higher structural high appears before W:
        replace H1 with the newer/higher high

STATE_HAVE_W
    if W is broken:
        invalidate and reset
    wait for structural high H2 such that H2 > H1

STATE_HAVE_H2
    if W is broken:
        invalidate and reset
    wait for structural low N1 such that N1 > W

STATE_HAVE_N1
    if W is broken:
        invalidate and reset
    wait for structural high R12
    require R12 < H2
    if candidate high >= H2:
        reject as continuation_without_valid_1_2_count

STATE_HAVE_R12
    if W is broken:
        invalidate and reset
    wait for structural low N2
    require N2 < N1 and N2 > W

STATE_HAVE_N2
    if W is broken:
        invalidate and reset
    wait for break above R12
    on break above R12:
        T12 = bar
        state = ARMED_AFTER_R12_BREAK

STATE_ARMED_AFTER_R12_BREAK
    if W is broken:
        invalidate, unless same-candle ambiguity rules apply
    wait for break above H2
    on break above H2:
        CONF = bar
        emit confirmed bullish F1
```

---

## 15. Bearish state machine

```text
STATE_IDLE
    wait for structural low L1

STATE_HAVE_L1
    wait for structural high W after L1
    W becomes protected waist
    if a lower structural low appears before W:
        replace L1 with the newer/lower low

STATE_HAVE_W
    if W is broken:
        invalidate and reset
    wait for structural low L2 such that L2 < L1

STATE_HAVE_L2
    if W is broken:
        invalidate and reset
    wait for structural high N1 such that N1 < W

STATE_HAVE_N1
    if W is broken:
        invalidate and reset
    wait for structural low R12
    require R12 > L2
    if candidate low <= L2:
        reject as continuation_without_valid_1_2_count

STATE_HAVE_R12
    if W is broken:
        invalidate and reset
    wait for structural high N2
    require N2 > N1 and N2 < W

STATE_HAVE_N2
    if W is broken:
        invalidate and reset
    wait for break below R12
    on break below R12:
        T12 = bar
        state = ARMED_AFTER_R12_BREAK

STATE_ARMED_AFTER_R12_BREAK
    if W is broken:
        invalidate, unless same-candle ambiguity rules apply
    wait for break below L2
    on break below L2:
        CONF = bar
        emit confirmed bearish F1
```

---

## 16. Detector pseudocode

### 16.1 Shared helpers

```text
is_high_node(node): node.type == HIGH
is_low_node(node):  node.type == LOW

is_known(node, current_bar): node.known_index <= current_bar.index
```

### 16.2 Bullish detector pseudocode

```text
for each symbol, timeframe, L:
    nodes = M0001_final_only_nodes(symbol, timeframe, L)
    bars  = chronological_bars(symbol, timeframe)

    bull = empty_candidate()

    for each bar in bars:
        reveal all nodes whose known_index == bar.index

        if bull.has_waist and bull.not_confirmed:
            check bull waist break on this bar

        if bull.state == IDLE:
            if revealed HIGH:
                bull.H1 = node
                bull.state = HAVE_H1

        elif bull.state == HAVE_H1:
            if revealed LOW after H1:
                bull.W = node
                bull.state = HAVE_W
            elif revealed HIGH and node.price > bull.H1.price:
                bull.H1 = node

        elif bull.state == HAVE_W:
            if waist broken:
                invalidate
            elif revealed HIGH and node.price > bull.H1.price + epsilon:
                bull.H2 = node
                bull.state = HAVE_H2

        elif bull.state == HAVE_H2:
            if waist broken:
                invalidate
            elif revealed LOW:
                if node.price > bull.W.price + epsilon:
                    bull.N1 = node
                    bull.open_count = 1
                    bull.state = HAVE_N1
                else:
                    invalidate_waist_or_no_protection

        elif bull.state == HAVE_N1:
            if waist broken:
                invalidate
            elif revealed HIGH:
                if node.price < bull.H2.price - epsilon:
                    bull.R12 = node
                    bull.state = HAVE_R12
                else:
                    reject_continuation_without_valid_1_2_count
                    reset_from_new_high(node)

        elif bull.state == HAVE_R12:
            if waist broken:
                invalidate
            elif revealed LOW:
                if node.price < bull.N1.price - epsilon and node.price > bull.W.price + epsilon:
                    bull.N2 = node
                    bull.open_count = 2
                    bull.state = HAVE_N2
                elif node.price <= bull.W.price + epsilon:
                    invalidate
                else:
                    wait_for_valid_N2_or_apply_noise_policy

        elif bull.state == HAVE_N2:
            if same_bar_confirms_and_breaks_waist:
                mark_ambiguous_and_reset
            elif waist broken:
                invalidate
            elif bar.high > bull.R12.price + epsilon:
                bull.T12 = bar
                bull.state = ARMED_AFTER_R12_BREAK

        elif bull.state == ARMED_AFTER_R12_BREAK:
            if same_bar_confirms_and_breaks_waist:
                mark_ambiguous_and_reset
            elif waist broken:
                invalidate
            elif bar.high > bull.H2.price + epsilon:
                bull.CONF = bar
                emit_event(bull)
                reset_or_seed_next_candidate
```

### 16.3 Bearish detector pseudocode

The bearish detector is the exact mirror:

```text
HIGH <-> LOW
>    <-> <
H1   <-> L1
H2   <-> L2
bull waist break: Low < W
bear waist break: High > W
bull R12 condition: R12 < H2
bear R12 condition: R12 > L2
bull trigger: High > R12
bear trigger: Low < R12
bull confirm: High > H2
bear confirm: Low < L2
```

---

## 17. Overlap, reset, and multiple candidates

### 17.1 One direction, one L

For the first version:

```text
keep at most one bullish candidate per L
keep at most one bearish candidate per L
```

This keeps the implementation simple and auditable.

### 17.2 Opposite directions

Bullish and bearish candidates may coexist on the same `L` if neither one violates its own waist.

Do not delete a bullish candidate just because a bearish partial candidate appears, unless the bullish waist is actually broken.

### 17.3 Direct continuation before valid N2

Bullish case:

```text
after H2 and N1, price makes a structural high >= H2 before valid N2
```

This means the market continued before completing the 1-2 F1 count.

Base classification:

```text
continuation_without_valid_1_2_count
```

Bearish mirror:

```text
after L2 and N1, price makes a structural low <= L2 before valid N2
```

### 17.4 Multiple possible R12 nodes

If multiple internal highs/lows appear between `N1` and `N2`, the base detector should use the latest valid internal reaction level before the valid `N2`, as long as it remains nested:

Bullish:

```text
R12 < H2
```

Bearish:

```text
R12 > L2
```

A stricter variant can use the first valid R12, but this must be explicitly marked as a variant.

---

## 18. Deduplication policy

Raw events must not be merged too early.

Suggested raw dedup key:

```text
symbol
timeframe
direction
L
W_time
H2_or_L2_time
N1_time
R12_time
N2_time
CONF_time
```

Cross-L duplicates should remain separate in the raw report.

Optional later confluence clustering can group events by:

```text
nearby W price
nearby H2/L2 price
nearby CONF time
same direction
adjacent L values
```

---

## 19. Event schema

Every confirmed, invalidated, rejected, and ambiguous candidate should be exportable.

```text
id
symbol
timeframe
direction
L

source_node_engine
node_reveal_contract
break_mode
epsilon_mode
candidate_status
invalid_reason
reject_reason
ambiguous_same_bar
same_bar_T12_CONF

H1_or_L1_time
H1_or_L1_known_time
H1_or_L1_price

W_time
W_known_time
W_price

H2_or_L2_time
H2_or_L2_known_time
H2_or_L2_price

N1_time
N1_known_time
N1_price

R12_time
R12_known_time
R12_price

N2_time
N2_known_time
N2_price

T12_time
T12_price
CONF_time
CONF_price

open_count_at_last_state
bars_H1_or_L1_to_W
bars_W_to_H2_or_L2
bars_H2_or_L2_to_N1
bars_N1_to_R12
bars_R12_to_N2
bars_N2_to_T12
bars_T12_to_CONF
bars_W_to_CONF

waist_distance
main_second_extreme_distance
n2_sweep_size
n2_protection_distance
n2_protection_ratio
internal_trigger_gap
internal_trigger_gap_ratio
confirmation_distance_from_N2
```

---

## 20. Structural measurements

Measurements are logged, not filtered, in the base version.

### 20.1 Bullish measurements

```text
waist_to_H2 = H2.price - W.price
h1_to_h2_extension = H2.price - H1.price
n1_depth_from_H2 = H2.price - N1.price
n2_sweep_size = N1.price - N2.price
n2_protection_distance = N2.price - W.price
n2_protection_ratio = (N2.price - W.price) / (H2.price - W.price)
internal_trigger_gap = H2.price - R12.price
internal_trigger_gap_ratio = (H2.price - R12.price) / (H2.price - W.price)
confirmation_distance_from_N2 = H2.price - N2.price
```

### 20.2 Bearish measurements

```text
waist_to_L2 = W.price - L2.price
l1_to_l2_extension = L1.price - L2.price
n1_depth_from_L2 = N1.price - L2.price
n2_sweep_size = N2.price - N1.price
n2_protection_distance = W.price - N2.price
n2_protection_ratio = (W.price - N2.price) / (W.price - L2.price)
internal_trigger_gap = R12.price - L2.price
internal_trigger_gap_ratio = (R12.price - L2.price) / (W.price - L2.price)
confirmation_distance_from_N2 = N2.price - L2.price
```

### 20.3 Why the `R12` gap matters

The `R12` gap measures how deeply nested the internal trigger is inside the main second extreme.

Bullish:

```text
internal_trigger_gap = H2 - R12
```

Bearish:

```text
internal_trigger_gap = R12 - L2
```

If the gap is zero or negative, the candidate is not a valid F1 in strict mode.

A small positive gap means the internal trigger is very close to the main confirmation level. A large gap means the market still has a significant distance between local recovery and full F1 confirmation.

This may become useful later, but it must not be used as a base filter yet.

---

## 21. Visual rendering contract

The chart must show the count and the difference between internal trigger and final confirmation.

### 21.1 Bullish visual objects

| Object | Required visual meaning |
|---|---|
| `W` | red protected waist line |
| `H1` | first roof marker, optional in compact mode |
| `H2` | main second roof line; final confirmation level |
| `R12` | internal roof line; must be visibly below `H2` |
| `N1` | label `1` under first internal low |
| `N2` | label `2` under second lower internal low |
| `T12` | small marker at internal trigger break |
| `CONF` | strong `F1` marker only at `H2` break |
| invalid candidate | faded red/grey debug object |

### 21.2 Bearish visual objects

| Object | Required visual meaning |
|---|---|
| `W` | red protected waist line above price |
| `L1` | first floor marker, optional in compact mode |
| `L2` | main second floor line; final confirmation level |
| `R12` | internal floor line; must be visibly above `L2` |
| `N1` | label `1` above first internal high |
| `N2` | label `2` above second higher internal high |
| `T12` | small marker at internal trigger break |
| `CONF` | strong `F1` marker only at `L2` break |
| invalid candidate | faded red/grey debug object |

### 21.3 Debug label text

Each confirmed F1 label should include:

```text
F1
DIR=BULL/BEAR
L=<value>
W=<price>
MAIN=<H2 or L2 price>
R12=<price>
N1=<price>
N2=<price>
R12_INSIDE_MAIN=true/false
```

It must be visually impossible to confuse `T12` with `CONF`.

---

## 22. Report contract

The first report must be structural, not profitable.

Required summary counts:

```text
candidate_count
confirmed_count
invalidated_count
rejected_count
ambiguous_same_bar_count
same_bar_T12_CONF_count

invalidated_before_N1
invalidated_before_N2
invalidated_after_N2_before_R12_break
invalidated_after_R12_before_main_break

rejected_R12_not_nested
rejected_continuation_without_valid_1_2
rejected_known_time_order

confirmation_rate
median_bars_W_to_CONF
median_n2_protection_ratio
median_internal_trigger_gap_ratio
```

Required segmentation:

```text
symbol
timeframe
L
direction
break_mode
epsilon_mode
```

Optional descriptive context tags:

```text
pre_context_hook_count
pre_context_two_hook_state
pre_context_violent_opposite_move
pre_context_last_regime_from_H0004_or_H0005
nearest_unconsumed_node_distance
nearest_zone_revisit_state
```

These context tags must not be base filters.

---

## 23. Random and null models for later validation

After F1 detection is mechanically stable, it must be compared against nulls.

Suggested nulls:

### 23.1 Time random

Random known-time bars with the same symbol, timeframe, and session distribution.

### 23.2 Node random

Random structural nodes from the same `L` stream and same direction class.

### 23.3 Matched-amplitude random

Match the distance from `W` to `H2/L2`.

### 23.4 Matched-duration random

Match the number of bars from `W` to `CONF`.

### 23.5 Matched-internal-gap random

Match the `R12` nested gap ratio:

Bullish:

```text
(H2 - R12) / (H2 - W)
```

Bearish:

```text
(R12 - L2) / (W - L2)
```

This prevents later results from being explained only by geometry or distance effects.

---

## 24. Later alpha questions

Only after visual audit and structural report stability:

```text
After confirmed F1, is forward MFE larger than matched random?
After confirmed F1, is MAE better contained by the waist?
Does F1 create directional memory?
Does F1 identify start-of-continuation paths?
Does N2 proximity to W predict explosive optionality?
Does R12 gap predict smoother or more explosive confirmation?
Does cross-L F1 confluence improve post-confirmation behavior?
Is F1 stronger after two hooks?
Is F1 stronger after a violent opposite move?
Is F1 useful as a regime label even without direct entry logic?
```

None of these are part of the F1 base definition.

---

## 25. Anti-overfit rules

The base F1 detector must not require:

```text
minimum ATR move
maximum ATR move
session filter
news filter
minimum slope
maximum bar count
specific symbol behavior
spread-dependent tuning
profit target
stop-loss
indicator confirmation
manual trendline confirmation
```

The base definition is only:

```text
known-time node order
protected waist
main second extreme
1-2 internal count
R12 nested inside main second extreme
internal trigger break
main second extreme break
explicit invalidation
explicit ambiguity handling
```

---

## 26. Relationship to previous modules

| Existing layer | Use in H0007 |
|---|---|
| `CP0001_structural_nodes` | source of structural pivots/nodes |
| `M0001 final-only live stream` | known-time node stream |
| `H0001` | nodes as decision-relevant locations |
| `H0002` | optional zone/revisit context |
| `H0004` | optional regime context |
| `H0005` | later directional-memory comparison |
| `H0006` | later optionality comparison |

H0007 is a grammar layer:

```text
nodes -> counted F structure -> visual audit -> random comparison -> later execution research
```

---

## 27. Implementation phases

### Phase 1 — README grammar lock

Lock the F1 definition:

```text
R12 break is not enough.
R12 must stay inside H2/L2.
Final confirmation requires H2/L2 break.
```

### Phase 2 — MQL detector skeleton

Suggested module:

```text
mql5/Experts/DecisionAlphaLab/M0007/M0007_FlagCountingF1.mq5
```

Suggested hypothesis id:

```text
H0007_FLAG_COUNTING_F1_START_STRUCTURE
```

### Phase 3 — visual debug

Draw:

```text
W line
H2/L2 line
R12 line
N1 label
N2 label
T12 marker
CONF marker
invalid candidates in debug mode
```

### Phase 4 — raw event export

Export confirmed, invalidated, rejected, and ambiguous candidate records.

### Phase 5 — structural report

Produce counts, distributions, and stability across `L`, direction, and epsilon modes.

### Phase 6 — post-confirmation behavior

Only after visual audit:

```text
MFE
MAE
path cleanliness
waist survival after confirmation
directional memory vs random
matched null comparison
```

---

## 28. Minimal acceptance checklist

The F1 detector is acceptable only if:

```text
[ ] Uses known-time nodes only.
[ ] Runs L=2 upward as separate passes.
[ ] Does not change L inside one candidate.
[ ] Detects bullish and bearish symmetrically.
[ ] Protects W until final confirmation.
[ ] Counts N1 and N2 correctly.
[ ] Requires bullish N2 < N1 and N2 > W.
[ ] Requires bearish N2 > N1 and N2 < W.
[ ] Requires bullish R12 < H2.
[ ] Requires bearish R12 > L2.
[ ] Logs R12 break separately as internal trigger.
[ ] Confirms only after H2/L2 break.
[ ] Handles same-candle ambiguity without favorable assumptions.
[ ] Draws R12 distinctly from H2/L2.
[ ] Exports all raw event fields.
[ ] Makes no trading or profitability claim.
```

---

## 29. One-sentence definitions

Bullish F1:

> A bullish F1 is a protected-waist start structure where price forms `H2` above `H1`, creates two internal lows with `N2 < N1` while preserving `W`, keeps the internal roof `R12` below `H2`, breaks `R12` only as an internal trigger, and confirms only by breaking `H2`.

Bearish F1:

> A bearish F1 is the mirrored protected-waist start structure where price forms `L2` below `L1`, creates two internal highs with `N2 > N1` while preserving `W`, keeps the internal floor `R12` above `L2`, breaks `R12` only as an internal trigger, and confirms only by breaking `L2`.

---

## 30. Compact formula

Bullish:

```text
H1 -> W -> H2 -> N1 -> R12 -> N2 -> T12 -> CONF

H2 > H1
W < H1
N1 > W
W < N2 < N1
N1 < R12 < H2
T12 = break(R12)
CONF = break(H2)
W must survive until CONF
```

Bearish:

```text
L1 -> W -> L2 -> N1 -> R12 -> N2 -> T12 -> CONF

L2 < L1
W > L1
N1 < W
W > N2 > N1
N1 > R12 > L2
T12 = break(R12)
CONF = break(L2)
W must survive until CONF
```
