# 03 — Divergence Detection Rules

## 1. Detection objective

For each enabled cycle group, detect whether the latest closed chart timeframe candle confirms that one symbol hunted a reference high/low while the other did not.

The model is symbol-symmetric and side-symmetric:

- high-side asymmetry creates bearish divergence;
- low-side asymmetry creates bullish divergence.

## 2. Required data

For every cycle group and every closed chart candle, the detector needs:

### 2.1 Current confirmation candle

For Symbol A:

```text
A_current_high
A_current_low
A_current_close_time
```

For Symbol B:

```text
B_current_high
B_current_low
B_current_close_time
```

The EA should use the just-closed candle on the chart timeframe. It should not evaluate the still-open candle.

### 2.2 Reference cycle levels

For reference cycle `R` in the same CG and same trading day:

```text
A_reference_high
A_reference_low
B_reference_high
B_reference_low
reference_cycle_start
reference_cycle_end
```

Baseline reference cycle:

```text
R = current_cycle_index - 1
```

## 3. Hunt rules

### 3.1 High hunt

```text
A_high_hunt = A_current_high >= A_reference_high
B_high_hunt = B_current_high >= B_reference_high
```

### 3.2 Low hunt

```text
A_low_hunt = A_current_low <= A_reference_low
B_low_hunt = B_current_low <= B_reference_low
```

### 3.3 Equality rule

Equal high/low is valid hunt.

Therefore operators are inclusive:

```text
>= for high hunt
<= for low hunt
```

### 3.4 No close requirement for hunt

The hunt itself does not require candle close beyond the general confirmation rule. The level may be touched intrabar. The event is only confirmed after the chart timeframe candle closes.

## 4. Divergence rules

### 4.1 Bearish divergence

A bearish divergence exists when high hunt is asymmetric.

```text
A_high_hunt != B_high_hunt
```

Cases:

| A high hunt | B high hunt | Divergence | Hunter | Clean | Trade |
|---|---|---|---|---|---|
| true | false | bearish | A | B | sell B |
| false | true | bearish | B | A | sell A |
| true | true | none | both | none | none |
| false | false | none | none | none | none |

### 4.2 Bullish divergence

A bullish divergence exists when low hunt is asymmetric.

```text
A_low_hunt != B_low_hunt
```

Cases:

| A low hunt | B low hunt | Divergence | Hunter | Clean | Trade |
|---|---|---|---|---|---|
| true | false | bullish | A | B | buy B |
| false | true | bullish | B | A | buy A |
| true | true | none | both | none | none |
| false | false | none | none | none | none |

## 5. Candle close confirmation

A divergence is not valid while the current chart timeframe candle is still open.

Implementation rule:

```text
Use bar shift 1 on the chart timeframe as the confirmation candle.
Never use bar shift 0 for signal confirmation.
```

The EA may watch intrabar values for visualization or diagnostics, but no trade signal can be produced until the candle closes.

## 6. Current cycle and confirmation candle relation

The confirmation candle belongs to a current CG cycle by its close time.

Recommended baseline:

```text
cycle_context = BuildCycleContext(confirmation_candle_close_time)
```

This means if a candle closes exactly on a cycle boundary, the close timestamp determines which cycle receives it. The implementation must define a deterministic boundary convention.

Recommended MQL5 convention:

```text
A bar with open time T and timeframe length TF closes at T + TF seconds.
Use close time minus 1 second for cycle membership if broker bar close is represented as next bar open time.
```

This avoids assigning a candle that ended at 18:30 to the 18:30–18:59 cycle when its price action occurred during 18:25–18:29.

## 7. Duplicate prevention

A signal should be uniquely identified by:

```text
trading_day_key
cycle_group_id
current_cycle_index
reference_cycle_index
side
hunter_symbol
clean_symbol
confirmation_bar_time
```

The EA should not open multiple trades for the same signal key.

If the same confirmation candle confirms both a bullish and bearish divergence in the same CG, the first implementation may allow both only if explicitly configured. Baseline safer rule:

```text
If both bullish and bearish divergences trigger in the same CG on the same confirmation candle, skip trading that CG for that candle and draw/debug as conflict.
```

This avoids simultaneous long/short ambiguity.

## 8. Reference levels and clean-symbol stop

For bearish divergence:

```text
hunter high touched hunter reference high
clean did not touch clean reference high
trade = sell clean
SL = clean reference high
```

For bullish divergence:

```text
hunter low touched hunter reference low
clean did not touch clean reference low
trade = buy clean
SL = clean reference low
```

## 9. Required event fields

Each detected divergence event should contain:

```text
strategy_id
trading_day_key
cg_name
cg_duration_minutes
current_cycle_index
current_cycle_start_broker
current_cycle_end_broker
reference_cycle_index
reference_cycle_start_broker
reference_cycle_end_broker
side
hunter_symbol
clean_symbol
trade_symbol
confirmation_time_broker
confirmation_bar_open_time_broker
hunter_reference_level
clean_reference_level
hunter_touch_price
clean_current_extreme
entry_direction
stop_loss
scheduled_exit_time_broker
is_trade_enabled
is_draw_enabled
signal_key
```

These fields should be available to both audit logs and drawing logic.

## 10. Edge cases

### 10.1 Both symbols hunt

No divergence. Both markets hunted the corresponding reference level.

### 10.2 Neither symbol hunts

No divergence.

### 10.3 One symbol lacks data

No trade. Log data error.

### 10.4 Reference cycle incomplete

The current cycle may be incomplete, but the reference cycle should be completed. If reference cycle is not completed, no signal.

### 10.5 Current cycle is first cycle of day

No signal, because there is no previous completed cycle in the same trading day.

### 10.6 Final incomplete cycle

Valid for detection and trading. Target is 17:00 NY, the day end.

### 10.7 Confirmation candle crosses cycle boundary

Use the candle's completed price action window to assign the cycle. Recommended: cycle membership based on `bar_open_time + period_seconds - 1 second`.

