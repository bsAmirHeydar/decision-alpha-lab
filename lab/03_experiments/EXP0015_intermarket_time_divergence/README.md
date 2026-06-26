# EXP0015 — Intermarket Time Divergence

## Core hypothesis

Time is the primary axis. A divergence is only meaningful when two correlated markets are compared on the same explicit time step.

The first target pair is S&P vs Nasdaq, usually `US500` and `NAS100` in MT5 broker naming. The module is symbol-agnostic and can compare any two markets.

## What is a divergence here?

A divergence event is recorded when, at a scheduled comparison step:

```text
origin market breaks/touches/hunts its selected high/low reference
AND
destination market does not break/touch/hunt its selected high/low reference
within the allowed lag window
```

High divergence:

```text
Origin takes a high, destination fails to take a high.
Suggested directional context: SELL / bearish divergence.
```

Low divergence:

```text
Origin takes a low, destination fails to take a low.
Suggested directional context: BUY / bullish divergence.
```

## Three axes of the experiment

### 1. Origin high/low probe

The origin probe is the current evaluation bar. It can be closed-bar only or include the live bar, controlled by:

```text
InpOriginBarMode
```

Trigger logic is controlled by:

```text
InpTriggerMode = WICK_TOUCH / CLOSE_BREAK / HUNT_REJECT_CLOSE
```

### 2. Destination/reference high/low

Both origin and destination references are configurable independently:

```text
InpOriginLevelSource
InpDestinationLevelSource
```

Supported references:

```text
PREVIOUS_CANDLE
ROLLING_LOOKBACK
L_NODE
CURRENT_SESSION
PREVIOUS_SESSION
CURRENT_DAY
PREVIOUS_DAY
```

The `L_NODE` option uses the existing DAL structural node engine:

```text
mql5/Include/StructuralNodes/DAL_StructuralNodeEngine.mqh
```

### 3. Time step schedule

Comparisons are made only on explicit steps:

```text
InpStepEveryBars
InpStepOffsetBars
InpDestinationLagBars
InpSignalValidBars
```

`InpDestinationLagBars` allows the second market to confirm within a few bars. If it confirms inside that lag window, no divergence is recorded. If it does not, the divergence becomes valid after the lag window.

## Session highs/lows

Session levels are supported directly. Defaults are broker-time New York cash-session assumptions for GMT+3 summer brokers:

```text
InpSessionStartHour   = 16
InpSessionStartMinute = 30
InpSessionEndHour     = 23
InpSessionEndMinute   = 0
```

Adjust these for your broker and DST rules.

## Expert

```text
mql5/Experts/IntermarketDivergence/IMD001_SPX_NDX_TimeDivergence.mq5
```

The expert is batch/bar-based. `OnTick()` is empty.

## Output

Default Common Files output:

```text
Common\Files\imd\EXP0015\imd001_divergence_events.csv
Common\Files\imd\EXP0015\imd001_summary.csv
```

Optional full step audit:

```text
Common\Files\imd\EXP0015\imd001_evaluated_steps.csv
```

## Event columns

Important columns:

```text
evaluation_time
valid_from_time
valid_until_time
valid_until_exclusive_time
window_end_reason
divergence_side
suggested_bias
origin_symbol
destination_symbol
origin_ref_price
destination_ref_price
origin_high / origin_low
destination_high / destination_low
origin_break_points
destination_break_points
divergence_gap_points
normalized_gap_ratio
```

## Current intended use

This experiment does not enter trades. It creates a clean, auditable divergence event dataset. Later experiments can test:

```text
- Does high divergence predict reversal / downside path?
- Does low divergence predict reversal / upside path?
- Which reference type is strongest: candle, rolling, node, session, or day?
- Which step size and lag window is most stable?
- Does the leading market matter: NAS100 leading SPX, or SPX leading NAS100?
```
