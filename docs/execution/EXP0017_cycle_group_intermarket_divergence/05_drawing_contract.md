# 05 — Drawing Contract

## 1. Purpose

The drawing layer visualizes confirmed divergence events without changing detection logic.

The user requested:

> Draw a line from the hunted high/low to the first candle that confirmed and closed the divergence, on the hunter symbol.

Because MQL5 objects are drawn on the chart where the EA is attached, the implementation must handle two-symbol visualization carefully.

## 2. Draw eligibility

A line is drawn only if all conditions are true:

```text
InpEnableDrawing == true
CG draw input == true
Divergence confirmed after candle close
Hunter symbol can be mapped to current chart or drawing mode supports symbolic object naming
```

If the EA is attached to Symbol A chart and hunter is Symbol B, there are two design options:

1. Draw all events on the attached chart but include hunter symbol in object label/name.
2. Restrict visual drawing to events whose hunter symbol equals chart symbol.

Baseline recommendation:

```text
Draw all events on the attached chart using the price scale of the hunter only when chart symbol == hunter symbol.
For non-chart hunter symbols, log the event and optionally create text label, but do not draw price-line on wrong scale.
```

This prevents visual distortion when SPXUSD and NDXUSD have different price scales.

Future version can use separate chart windows or ChartOpen/ChartSetSymbolPeriod for per-symbol drawings.

## 3. Draw object type

Recommended object:

```cpp
OBJ_TREND
```

A trend line is used because it can connect:

- point 1: hunted reference level at the hunter's first touch candle/time;
- point 2: same price level or confirmation price at the confirmation candle close time.

User requested line from the high/low that was hunted to the first candle that confirmed and closed the divergence.

Recommended interpretation:

```text
Point 1:
    time  = first touch candle time on hunter symbol
    price = hunted reference level
Point 2:
    time  = confirmation candle close time
    price = hunted reference level
```

This creates a horizontal or near-horizontal reference line from the hunted level to confirmation.

Alternative interpretation:

```text
Point 2 price = hunter candle close or hunter touch price
```

Baseline should use the reference level because the semantic object is the hunted high/low line.

## 4. High-side drawing

For bearish divergence:

```text
hunter touched/crossed reference high
line starts at hunter reference high
line ends at confirmation candle close time
```

Line price:

```text
hunter_reference_high
```

Label example:

```text
cg_180m SELL divergence | Hunter: SPXUSD | Clean: NDXUSD
```

## 5. Low-side drawing

For bullish divergence:

```text
hunter touched/crossed reference low
line starts at hunter reference low
line ends at confirmation candle close time
```

Line price:

```text
hunter_reference_low
```

Label example:

```text
cg_30m BUY divergence | Hunter: NDXUSD | Clean: SPXUSD
```

## 6. Color

Every CG has independent color input:

```cpp
InpCG_180m_Color = clrBlack;
```

Default for all:

```text
black
```

This allows the user to visually separate large and small cycle groups later by color.

## 7. Object naming

Object names must be deterministic and unique.

Recommended format:

```text
CGDIV_<strategy_id>_<trading_day_key>_<cg_name>_<cycle_index>_<side>_<hunter>_<clean>_<bar_time>
```

Example:

```text
CGDIV_EXP0017_20260709_cg_180m_2_SELL_SPXUSD_NDXUSD_20260709_213000
```

## 8. Duplicate-safe drawing

Before creating an object:

```cpp
if(ObjectFind(0, object_name) >= 0)
    skip_create;
else
    create_object;
```

The drawing module should not create duplicate lines on every tick.

## 9. Metadata text

Recommended optional text label or tooltip:

```text
CG: cg_180m
Side: SELL
Hunter: SPXUSD
Clean: NDXUSD
Reference: previous cycle high
Ref price: 6420.50
Confirm: 2026-07-09 21:30 broker
Target exit: 2026-07-09 23:59 broker
Trade: enabled
```

In MQL5, object description or text can be used depending on object type.

## 10. Drawing cleanup

Because the strategy only uses the current trading day for entries, drawings may be managed by one of two policies:

### Policy A — persistent drawings

Keep drawings on chart until user removes them.

Pros:

- Visual audit remains.

Cons:

- Chart can become cluttered.

### Policy B — same-day cleanup

Remove prior trading-day objects at new 18:00 NY day start.

Pros:

- Matches same-day signal rule.
- Cleaner chart.

Cons:

- Historical visual audit is lost unless logs exist.

Baseline recommendation:

```text
Keep drawings by default; add optional same-day cleanup input later.
```

## 11. Drawing is non-authoritative

The drawing module must never be the source of truth for trading.

Correct flow:

```text
Detection -> Event -> Signal Registry -> Drawing Manager
Detection -> Event -> Trade Router
```

Incorrect flow:

```text
Object on chart -> trade logic
```

