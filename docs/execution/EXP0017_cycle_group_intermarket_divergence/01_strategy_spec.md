# 01 — Strategy Specification

## 1. Objective

Build an independent MQL5 expert that trades divergence between two symbols using predefined time cycle groups.

The expert watches two symbols. For each enabled cycle group, it partitions the New York trading day into fixed-duration cycles. Within the current trading day, when a cycle reference high or low is hunted by one symbol but not by the other, a divergence can be formed. The divergence becomes valid only after the chart timeframe candle closes.

The expert then enters on the symbol that did not hunt the reference level.

## 2. Symbols

The expert has two symbol inputs:

```text
Symbol A default: SPXUSD
Symbol B default: NDXUSD
```

The model treats both symbols symmetrically.

There is no permanent leader/follower role. For every event:

- hunter symbol = the symbol that touched or crossed the reference high/low;
- clean symbol = the symbol that did not touch or cross the corresponding reference high/low;
- trade symbol = clean symbol.

## 3. Trading day

The strategy day is a New York trading day:

```text
Start: 18:00 New York time
End:   17:00 New York time, next calendar day
```

The trading day is 23 hours long:

```text
23 hours = 1380 minutes
```

Only signals belonging to the current trading day are checked. The expert does not analyze previous trading days for entry.

## 4. Cycle groups

A cycle group is a repeated partition of the current 18:00-to-17:00 New York trading day into fixed minute blocks.

Supported cycle groups:

```text
cg_3m
cg_5m
cg_9m
cg_10m
cg_15m
cg_18m
cg_20m
cg_24m
cg_30m
cg_40m
cg_45m
cg_60m
cg_72m
cg_90m
cg_120m
cg_150m
cg_180m
cg_240m
cg_300m
cg_360m
cg_720m
```

Examples:

```text
cg_30m:
18:00–18:29
18:30–18:59
19:00–19:29
...
```

```text
cg_180m:
18:00–20:59
21:00–23:59
00:00–02:59
...
```

If the cycle duration does not evenly divide 1380 minutes, the final cycle of the day is allowed to be incomplete.

## 5. Reference level

For any current cycle in a cycle group, the reference level is taken from a previous completed cycle inside the same current trading day.

The first implementation should use this baseline doctrine:

```text
Current cycle compares against immediately previous completed cycle of the same CG.
```

This keeps the first expert deterministic and avoids multiple-reference ambiguity.

Future versions may add:

- compare against all previous cycles in same day;
- compare against selected previous N cycles;
- compare against session subwindows;
- compare against weighted reference pools.

These are future extensions, not part of the first specification.

## 6. Hunt definition

A hunt is touch-only.

High hunt:

```text
current_candle_high >= reference_high
```

Low hunt:

```text
current_candle_low <= reference_low
```

Important rules:

- No candle close is required for the hunt itself.
- Touch is enough.
- Crossing is enough.
- Equal high is a high hunt.
- Equal low is a low hunt.
- No tolerance is applied in the baseline model.

## 7. Divergence definition

A divergence is formed only after the chart timeframe candle closes.

The EA runs on one chart timeframe. That timeframe is the confirmation timeframe. If the EA is attached to M5, an event can be confirmed only when the relevant M5 candle closes.

### 7.1 Bullish divergence / buy setup

Bullish divergence is based on low-side hunt asymmetry.

```text
One symbol hunts the reference low.
The other symbol does not hunt the corresponding reference low.
The chart timeframe candle closes.
=> bullish divergence is confirmed.
=> buy clean symbol.
```

### 7.2 Bearish divergence / sell setup

Bearish divergence is based on high-side hunt asymmetry.

```text
One symbol hunts the reference high.
The other symbol does not hunt the corresponding reference high.
The chart timeframe candle closes.
=> bearish divergence is confirmed.
=> sell clean symbol.
```

## 8. Entry timing

The expert waits for the confirmation candle to close.

At the next runtime pulse after candle close:

```text
If divergence is confirmed
and the CG trade input is ON
and no duplicate signal has already been traded
then enter on clean symbol.
```

The entry is market execution on the clean symbol.

## 9. Stop-loss

The stop-loss is the reference level of the divergence on the clean symbol.

For buy:

```text
SL = reference low of clean symbol
```

For sell:

```text
SL = reference high of clean symbol
```

No buffer is part of the baseline spec.

## 10. Target

The target is temporal, not price-based.

```text
Exit at the end of the current cycle in that cycle group.
```

This means the EA needs a scheduled close for positions whose lifecycle target is cycle-end.

The first implementation should interpret target as:

```text
Close the position at or immediately after current CG cycle end.
```

No take-profit price is required by the baseline model. The target is a time exit.

## 11. Risk

Risk per trade:

```text
1% of current equity
```

Position volume must be calculated from:

```text
Equity × 1%
Distance from entry to stop
Tick value / tick size of clean symbol
Broker min/max/step volume constraints
```

## 12. Same-day-only rule

The EA only processes signals inside the current New York trading day.

Allowed:

- use earlier completed cycles from the same current 18:00–17:00 day;
- trade a divergence confirmed during the current trading day;
- close positions at current cycle end.

Not allowed:

- use yesterday's cycles as reference;
- carry unconfirmed divergence state from yesterday into today;
- create new entries after 17:00 NY from old references.

## 13. Core invariants

The following rules are hard rules:

1. Hunt is touch-only.
2. Equal level counts as hunt.
3. Divergence confirmation requires candle close.
4. Buy divergence uses low hunt asymmetry.
5. Sell divergence uses high hunt asymmetry.
6. Trade is opened on clean symbol, not hunter symbol.
7. Stop is the reference level on clean symbol.
8. Target is current cycle end.
9. Risk is 1% equity.
10. No previous trading day data is needed for entry.
11. Each CG has independent Trade ON/OFF, Draw ON/OFF, and Draw Color inputs.

