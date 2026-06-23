# H0007 — Flag Counting / F1 Start Structure

> Status: design lock, no execution edge claimed yet.  
> Layer: structural grammar on top of the M0001 known-time node stream.  
> Scope of this document: define F1 only. F2 and F3 are intentionally out of scope until F1 is mechanically stable.

---

## 1. Core idea

The working thesis is:

> The market can be parsed as a chain of flags, but a flag must not remain a discretionary drawing. It must become a countable structural grammar.

H0007 introduces the first grammar object: **F1**.

F1 is not a trade setup yet. It is not a signal, not a win-rate claim, and not a target model. F1 is a **known-time structural event** that can be counted, drawn, audited, and later tested against random or alternative structural baselines.

The first objective is therefore simple:

> Can we detect F1 mechanically from structural nodes without future leakage and draw the same count on the chart that a human would mark by hand?

---

## 2. Reference sketches

Bullish F1 sketch:

![Bullish F1 sketch](../../assets/H0007/f1.png)

Hook-hook-to-F1 context sketch:

![Hook hook F1 sketch](../../assets/H0007/flag-hook-hook-f1.png)

These drawings are not the algorithm. They are visual references for the topology that the algorithm must reproduce.

---

## 3. Critical definition lock

The F1 confirmation is **not** only the break of the roof between node 1 and node 2.

For bullish F1:

1. price must break the **internal roof between 1 and 2**, and
2. price must also break the **main second roof**.

The internal roof break only arms or locally triggers the structure. The F1 is confirmed only after the main second roof is broken.

For bearish F1 the mirror rule applies:

1. price must break the **internal floor between 1 and 2**, and
2. price must also break the **main second floor**.

This is the most important correction in the F1 grammar.

---

## 4. Terminology

### 4.1 Bullish names

| Symbol | Name | Meaning |
|---|---|---|
| `H0` | first roof | first structural high after the initial upward movement |
| `W` | waist | protected structural low after `H0`; this is the red line in the sketch |
| `H2` | main second roof | structural high after `W` that breaks `H0`; this is the main F1 roof that must later be broken again |
| `N1` | count node 1 | first internal structural low after `H2` |
| `R12` | internal roof | structural high between `N1` and `N2` |
| `N2` | count node 2 | second internal structural low, below `N1`, but above `W` |
| `T12` | internal trigger | first break above `R12` after `N2` |
| `CONF` | F1 confirmation | first break above `H2` after `N2` |

### 4.2 Bearish names

| Symbol | Name | Meaning |
|---|---|---|
| `L0` | first floor | first structural low after the initial downward movement |
| `W` | waist | protected structural high after `L0`; this is the bearish red line |
| `L2` | main second floor | structural low after `W` that breaks `L0`; this is the main F1 floor that must later be broken again |
| `N1` | count node 1 | first internal structural high after `L2` |
| `R12` | internal floor | structural low between `N1` and `N2` |
| `N2` | count node 2 | second internal structural high, above `N1`, but below `W` |
| `T12` | internal trigger | first break below `R12` after `N2` |
| `CONF` | F1 confirmation | first break below `L2` after `N2` |

`R12` means "reaction level between 1 and 2". In bullish mode it is a roof. In bearish mode it is a floor.

---

## 5. Structural source contract

F1 must be built from the same structural-node discipline as the rest of Decision Alpha Lab.

Required source:

```text
M0001 final-only structural node stream
```

Required timing contract:

```text
A pivot may be visually anchored at its pivot candle,
but the algorithm may only use it after its known/reveal time.
```

If a pivot uses `L`, then:

```text
pivot_index = i
known_index = i + L
```

The chart can draw the node at `i`, but the state machine cannot react to it before `i + L`.

This keeps F1 compatible with the no-future standard used in H0004, H0005, and the atomic replay work.

---

## 6. Scale parameter `L`

F1 is counted on a specific node scale.

```text
L_min = 2
L_max = configurable
```

The first implementation should run separate passes for each `L`:

```text
L = 2
L = 3
L = 4
...
L = L_max
```

A single F1 candidate must not change `L` while it is forming.

Later, cross-scale clustering can be added:

```text
same F1 found on multiple nearby L values => stronger structural confluence
```

But the first version must stay simple:

```text
one F1 = one direction + one L + one known-time node sequence
```

---

## 7. Bullish F1 definition

A bullish F1 candidate is valid only if the following sequence exists in known-time order:

```text
H0 -> W -> H2 -> N1 -> R12 -> N2 -> T12 -> CONF
```

The strict topology is:

```text
H2 > H0
W  < H0
N1 > W
R12 > N1
R12 < H2
N2 < N1
N2 > W
T12 breaks above R12
CONF breaks above H2
```

The protected-waist rule is absolute in the base mode:

```text
From the moment W exists until CONF,
no candle may break W.
```

For the bullish wick-strict base mode:

```text
if Low < W_price - epsilon:
    invalidate candidate
```

The structure is not confirmed at `T12`. It is only armed. Final F1 confirmation occurs at `CONF`:

```text
if High > H2_price + epsilon after N2:
    confirm bullish F1
```

---

## 8. Bearish F1 definition

A bearish F1 candidate is valid only if the following sequence exists in known-time order:

```text
L0 -> W -> L2 -> N1 -> R12 -> N2 -> T12 -> CONF
```

The strict topology is:

```text
L2 < L0
W  > L0
N1 < W
R12 < N1
R12 > L2
N2 > N1
N2 < W
T12 breaks below R12
CONF breaks below L2
```

The protected-waist rule is absolute in the base mode:

```text
From the moment W exists until CONF,
no candle may break W.
```

For the bearish wick-strict base mode:

```text
if High > W_price + epsilon:
    invalidate candidate
```

The structure is not confirmed at `T12`. It is only armed. Final F1 confirmation occurs at `CONF`:

```text
if Low < L2_price - epsilon after N2:
    confirm bearish F1
```

---

## 9. What counts as a break?

The base version is intentionally strict because the waist is defined as a level that must not be violated.

### 9.1 Base mode

```text
break_mode = wick_strict
```

Bullish invalidation:

```text
Low < W_price - epsilon
```

Bearish invalidation:

```text
High > W_price + epsilon
```

Bullish confirmation:

```text
High > H2_price + epsilon
```

Bearish confirmation:

```text
Low < L2_price - epsilon
```

### 9.2 Stability modes for later testing

The implementation should allow these modes, but the base report must begin with wick-strict:

```text
wick_strict
close_break
epsilon_break
```

Suggested epsilon sensitivity grid:

```text
epsilon = 0
epsilon = 1 * point
epsilon = 1 * spread
epsilon = 0.05 * ATR
epsilon = 0.10 * ATR
```

No result should be trusted if it only exists under one fragile epsilon setting.

---

## 10. Same-candle ambiguity rule

In historical OHLC data, if a candle both confirms F1 and violates the waist, the intrabar order is unknown.

Example bullish ambiguity:

```text
same candle:
    High > H2_price
    Low  < W_price
```

Default rule:

```text
mark candidate as ambiguous_same_bar
exclude it from the main confirmed sample
```

Do not assume the favorable order. Do not convert it into a win. Do not use it as a clean F1.

Optional conservative mode:

```text
waist violation wins over confirmation
```

But the official research report should log ambiguous cases separately.

---

## 11. Candidate state machine

### 11.1 Bullish state machine

```text
STATE_IDLE
    wait for structural high H0

STATE_HAVE_H0
    wait for structural low W after H0
    set W as protected waist

STATE_HAVE_W
    if W is broken -> invalidate and reset
    wait for structural high H2 such that H2 > H0

STATE_HAVE_H2
    if W is broken -> invalidate and reset
    wait for structural low N1 after H2

STATE_HAVE_N1
    if W is broken -> invalidate and reset
    wait for structural high R12 after N1
    require R12 < H2 for a clean nested F1 count

STATE_HAVE_R12
    if W is broken -> invalidate and reset
    wait for structural low N2 after R12
    require N2 < N1 and N2 > W

STATE_HAVE_N2
    if W is broken -> invalidate and reset
    wait for break above R12
    once broken, mark T12 and move to ARMED

STATE_ARMED_AFTER_R12_BREAK
    if W is broken -> invalidate or ambiguous if same bar as CONF
    wait for break above H2
    if H2 is broken -> CONFIRMED_F1
```

### 11.2 Bearish state machine

```text
STATE_IDLE
    wait for structural low L0

STATE_HAVE_L0
    wait for structural high W after L0
    set W as protected waist

STATE_HAVE_W
    if W is broken -> invalidate and reset
    wait for structural low L2 such that L2 < L0

STATE_HAVE_L2
    if W is broken -> invalidate and reset
    wait for structural high N1 after L2

STATE_HAVE_N1
    if W is broken -> invalidate and reset
    wait for structural low R12 after N1
    require R12 > L2 for a clean nested F1 count

STATE_HAVE_R12
    if W is broken -> invalidate and reset
    wait for structural high N2 after R12
    require N2 > N1 and N2 < W

STATE_HAVE_N2
    if W is broken -> invalidate and reset
    wait for break below R12
    once broken, mark T12 and move to ARMED

STATE_ARMED_AFTER_R12_BREAK
    if W is broken -> invalidate or ambiguous if same bar as CONF
    wait for break below L2
    if L2 is broken -> CONFIRMED_F1
```

---

## 12. Pseudocode

### 12.1 Shared helpers

```text
is_bull_break(level, bar):
    return bar.high > level + epsilon

is_bear_break(level, bar):
    return bar.low < level - epsilon

is_bull_waist_broken(W, bar):
    return bar.low < W.price - epsilon

is_bear_waist_broken(W, bar):
    return bar.high > W.price + epsilon
```

### 12.2 Bullish detector

```text
for each symbol, timeframe, L:
    nodes = final_only_known_time_nodes(symbol, timeframe, L)
    bars  = known_time_bars(symbol, timeframe)

    candidate = empty

    for each event in chronological known-time order:

        update candidate with newly known nodes
        check every new closed bar for waist break, R12 break, and H2 break

        if state == IDLE:
            if event is HIGH:
                H0 = event
                state = HAVE_H0

        elif state == HAVE_H0:
            if event is LOW after H0:
                W = event
                state = HAVE_W
            elif event is HIGH higher than H0:
                H0 = event

        elif state == HAVE_W:
            if waist broken:
                reset
            elif event is HIGH and event.price > H0.price + epsilon:
                H2 = event
                state = HAVE_H2

        elif state == HAVE_H2:
            if waist broken:
                invalidate
            elif event is LOW and event.price > W.price + epsilon:
                N1 = event
                state = HAVE_N1
            elif event is LOW and event.price <= W.price + epsilon:
                invalidate

        elif state == HAVE_N1:
            if waist broken:
                invalidate
            elif event is HIGH:
                if event.price < H2.price - epsilon:
                    R12 = event
                    state = HAVE_R12
                else:
                    # H2 was broken before N2 existed. This is not F1.
                    reject_as_continuation_without_1_2
                    reset_from_new_high(event)

        elif state == HAVE_R12:
            if waist broken:
                invalidate
            elif event is LOW:
                if event.price < N1.price - epsilon and event.price > W.price + epsilon:
                    N2 = event
                    state = HAVE_N2
                elif event.price <= W.price + epsilon:
                    invalidate
                else:
                    # Not a valid lower second node yet.
                    keep_waiting_or_update_noise_rule

        elif state == HAVE_N2:
            if same_bar_confirms_and_breaks_waist:
                mark_ambiguous_and_reset
            elif waist broken:
                invalidate
            elif bar.high > R12.price + epsilon:
                T12 = bar
                state = ARMED_AFTER_R12_BREAK

        elif state == ARMED_AFTER_R12_BREAK:
            if same_bar_confirms_and_breaks_waist:
                mark_ambiguous_and_reset
            elif waist broken:
                invalidate
            elif bar.high > H2.price + epsilon:
                CONF = bar
                emit bullish F1
                reset_or_start_new_candidate_from_CONF_context
```

### 12.3 Bearish detector

The bearish detector is the exact mirror:

```text
HIGH <-> LOW
>    <-> <
waist break: High > W
internal trigger: Low < R12
final confirmation: Low < L2
```

---

## 13. Overlap and reset policy

F1 candidates can overlap. The first implementation should avoid too much intelligence and use deterministic rules.

### 13.1 Same direction overlap

If a new stronger `H0` appears before `W`, update `H0`.

If `H2` is broken before `N2` exists, the candidate is not an F1. It is a direct continuation without a completed 1-2 count.

If multiple possible `R12` nodes appear between `N1` and `N2`, use the latest clean structural high before valid `N2`, unless a stricter variant is explicitly being tested.

### 13.2 Opposite direction overlap

Bullish and bearish candidates may exist at the same time on different `L` values.

Within the same `L`, keep one bullish candidate and one bearish candidate independently. Do not let a bearish partial count automatically delete a bullish partial count unless it violates the bullish waist.

### 13.3 Deduplication

Confirmed F1 events should be deduplicated only after detection.

Suggested dedup key:

```text
symbol
timeframe
direction
L
W_time
H2_or_L2_time
N1_time
N2_time
CONF_time
```

Cross-L duplicates must not be merged in the raw report. They should be reported separately first, then clustered in an optional confluence report.

---

## 14. Output event schema

Every F1 event must be exported as a complete record.

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

H0_or_L0_time
H0_or_L0_known_time
H0_or_L0_price

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

candidate_status
invalid_reason
ambiguous_same_bar

bars_H0_to_W
bars_W_to_H2_or_L2
bars_H2_or_L2_to_N1
bars_N1_to_R12
bars_R12_to_N2
bars_N2_to_T12
bars_T12_to_CONF
bars_W_to_CONF

waist_distance
main_roof_or_floor_distance
n2_sweep_size
n2_protection_distance
n2_protection_ratio
internal_trigger_distance
confirmation_distance_from_N2
```

---

## 15. Structural measurements

### 15.1 Bullish measurements

```text
waist_to_H2 = H2.price - W.price
n2_sweep_size = N1.price - N2.price
n2_protection_distance = N2.price - W.price
n2_protection_ratio = (N2.price - W.price) / (H2.price - W.price)
internal_roof_gap = H2.price - R12.price
confirm_distance_from_N2 = H2.price - N2.price
```

### 15.2 Bearish measurements

```text
waist_to_L2 = W.price - L2.price
n2_sweep_size = N2.price - N1.price
n2_protection_distance = W.price - N2.price
n2_protection_ratio = (W.price - N2.price) / (W.price - L2.price)
internal_floor_gap = R12.price - L2.price
confirm_distance_from_N2 = N2.price - L2.price
```

These measurements are not filters in the base version. They are logged for later stability and distribution analysis.

---

## 16. Visual rendering contract

The chart must show the count, not only the final signal.

### 16.1 Bullish visual objects

| Object | Visual rule |
|---|---|
| `W` waist | red horizontal line from `W` to invalidation or confirmation |
| `H2` main second roof | main F1 roof line; final confirmation level |
| `R12` internal roof | dashed or thinner line between `N1` and `N2`; local trigger level |
| `N1` | yellow label `1` at the first internal low |
| `N2` | yellow label `2` at the second lower internal low |
| `T12` | small marker when `R12` breaks |
| `CONF` | strong F1 marker only when `H2` breaks |
| invalidated candidate | grey/red faded objects, optional in debug mode |

### 16.2 Bearish visual objects

| Object | Visual rule |
|---|---|
| `W` waist | red horizontal line above price from `W` to invalidation or confirmation |
| `L2` main second floor | main F1 floor line; final confirmation level |
| `R12` internal floor | dashed or thinner line between `N1` and `N2`; local trigger level |
| `N1` | label `1` at the first internal high |
| `N2` | label `2` at the second higher internal high |
| `T12` | small marker when `R12` breaks |
| `CONF` | strong F1 marker only when `L2` breaks |

### 16.3 Required chart debug text

Each confirmed F1 label should include at least:

```text
F1
DIR=BULL/BEAR
L=<value>
W=<price>
MAIN=<H2 or L2 price>
N1=<price>
N2=<price>
```

The visual must make it impossible to confuse `R12` break with full F1 confirmation.

---

## 17. Report contract

The first report must answer structural questions, not profitability questions.

Required counts:

```text
candidate_count
confirmed_count
invalidated_before_N1
invalidated_before_N2
invalidated_after_N2_before_R12_break
invalidated_after_R12_before_main_break
ambiguous_same_bar_count
confirmation_rate
median_bars_W_to_CONF
median_n2_protection_ratio
median_internal_roof_or_floor_gap
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

Optional context tags from existing modules:

```text
pre_context_hook_count
pre_context_last_regime_from_H0004_or_H0005
nearest_unconsumed_node_distance
nearest_zone_revisit_state
```

These tags must not be used as filters in the first base report. They are only descriptive.

---

## 18. Later alpha questions

After F1 is mechanically stable, the next research layer can ask:

```text
After confirmed F1, is forward MFE larger than random?
After confirmed F1, is MAE smaller or better contained by the waist?
Does F1 increase directional memory?
Does F1 identify the start of continuation paths?
Does N2 proximity to waist predict explosive optionality?
Does cross-L F1 confluence improve post-confirmation behavior?
Is F1 better after two hooks?
Is F1 better after a violent opposite move?
```

None of these are part of the base definition.

---

## 19. Random and null models for future validation

When F1 is later tested as a possible alpha object, it must be compared against nulls.

Suggested nulls:

### 19.1 Time random

Randomly choose known-time bars with the same symbol, timeframe, and session distribution.

### 19.2 Node random

Randomly choose structural nodes from the same `L` stream and direction class.

### 19.3 Matched-distance random

Match the distance from `W` to `H2/L2`, then compare forward behavior from random structural locations with similar amplitude.

### 19.4 Matched-duration random

Match the number of bars from `W` to `CONF`, then compare post-event behavior.

The first F1 implementation only needs to export enough fields to make these nulls possible later.

---

## 20. Anti-overfit rules

The base F1 detector must not include these as required filters:

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
```

The first version is topology only:

```text
node order
protected waist
1-2 count
internal trigger break
main second roof/floor break
known-time causality
```

Amplitude, volatility, session, and execution filters can be tested later, but they must not define F1.

---

## 21. Relationship to previous project modules

H0007 depends on existing layers but does not replace them.

| Existing layer | Use in H0007 |
|---|---|
| `CP0001_structural_nodes` | source of pivots/nodes |
| `M0001 final-only live stream` | known-time structural stream |
| `H0001` | philosophical basis: nodes are decision-relevant |
| `H0002` | optional context: revisits, zones, consumed nodes |
| `H0004` | optional context: regime memory before/after F1 |
| `H0005` | later directional-memory comparison after F1 |
| `H0006` | optionality comparison after reversal/explosive states |

H0007 is a grammar layer:

```text
nodes -> counted F structure -> later regime/execution tests
```

---

## 22. Implementation plan

### Phase 1 — README and grammar lock

Deliver this document and lock the corrected F1 definition:

```text
R12 break is not enough.
Main second roof/floor break is required.
```

### Phase 2 — detector skeleton

Add an MQL module that reads the M0001 final node stream and maintains bullish and bearish F1 candidate states per `L`.

Suggested module name:

```text
M0007_FlagCountingF1.mq5
```

Suggested hypothesis id:

```text
H0007_FLAG_COUNTING_F1_START_STRUCTURE
```

### Phase 3 — visual debug

Draw candidates and confirmed F1 structures on chart:

```text
waist line
main second roof/floor line
internal R12 line
1/2 labels
T12 marker
CONF marker
invalid candidate debug mode
```

### Phase 4 — structural report

Export raw event records and summary counts. No trading metrics yet.

### Phase 5 — post-confirmation behavior

Only after visual and count audit passes, evaluate forward behavior:

```text
MFE
MAE
path cleanliness
waist survival after confirmation
directional memory vs random
```

---

## 23. Minimal acceptance checklist

The F1 detector is acceptable only if all of these are true:

```text
[ ] Uses known-time nodes, not future-known pivots.
[ ] Runs from L=2 upward as separate scale passes.
[ ] Does not change L inside one candidate.
[ ] Detects bullish and bearish F1 symmetrically.
[ ] Protects W until final confirmation.
[ ] Logs internal R12 break separately.
[ ] Confirms only after H2/L2 break.
[ ] Handles same-candle ambiguity without favorable assumptions.
[ ] Draws N1 and N2 correctly on chart.
[ ] Draws the main second roof/floor distinctly from R12.
[ ] Exports full event fields.
[ ] Makes no profitability claim in the base report.
```

---

## 24. One-sentence definition

Bullish F1:

> A bullish F1 is a protected-waist start structure where price forms a main second roof above the first roof, creates two internal lows with `N2 < N1` while preserving the waist, breaks the internal roof between 1 and 2, and finally confirms only by breaking the main second roof.

Bearish F1:

> A bearish F1 is the mirrored protected-waist start structure where price forms a main second floor below the first floor, creates two internal highs with `N2 > N1` while preserving the waist, breaks the internal floor between 1 and 2, and finally confirms only by breaking the main second floor.
