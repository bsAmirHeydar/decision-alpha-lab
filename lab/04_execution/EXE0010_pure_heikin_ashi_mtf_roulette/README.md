# EXE0010 — Pure Heikin Ashi MTF Roulette

## Purpose

This execution module is a pure Heikin Ashi entry model.

It does not use the previous structural continuation/reversal regime modules.

The entry decision is based only on:

- current-forming higher-timeframe Heikin Ashi color,
- completed lower-timeframe Heikin Ashi color flip,
- Roulette risk sizing.

---

## Timeframes

Default inputs:

- Entry timeframe: `PERIOD_M1`
- Direction timeframe: `PERIOD_M10`

The current-forming M10 Heikin Ashi candle defines the allowed trade direction.

The closed M1 Heikin Ashi flip defines the actual entry trigger.

---

## Buy Logic

A buy is allowed only when:

1. Current-forming M10 Heikin Ashi candle is green.
2. Last closed M1 Heikin Ashi candle is green.
3. The previous closed M1 Heikin Ashi candle was red.
4. The max-open-trade limit allows a new position.

In short:

```text
HTF current HA = green
M1 previous closed HA = red
M1 last closed HA = green
=> BUY
```

---

## Sell Logic

A sell is allowed only when:

1. Current-forming M10 Heikin Ashi candle is red.
2. Last closed M1 Heikin Ashi candle is red.
3. The previous closed M1 Heikin Ashi candle was green.
4. The max-open-trade limit allows a new position.

In short:

```text
HTF current HA = red
M1 previous closed HA = green
M1 last closed HA = red
=> SELL
```

---

## Closed Trigger Rule

Only completed lower-timeframe Heikin Ashi candles are allowed to trigger entries.

The module does not enter from the still-forming M1 candle.

---

## Risk Model

The execution uses `DAL_ExecRouletteRisk.mqh`.

Roulette risk returns money risk only.

The execution module converts that money risk into lot size using the existing `DAL_ExecCalculateRiskVolume` primitive.

Default Roulette inputs:

```text
Initial Risk Percent = 10.0
Save Profit Factor = 0.50
Persist State = true
```

Correct Roulette cycle behavior:

- Balance is locked at cycle start.
- Base risk is fixed from locked balance.
- Losing below the protected floor does not reduce risk.
- Risk remains base risk until the cycle first becomes profitable.
- After profit, risk can expand from `current_balance - floor_balance`.
- After profit then realized balance drop, the cycle resets to the new balance.
- Consecutive losses after reset keep the new base risk.

---

## Stop and Take Profit

The module uses a fixed-R target.

Default:

```text
RewardR = 2.0
```

Stop is derived from the recent closed lower-timeframe Heikin Ashi / real candle extreme.

Default:

```text
StopLookbackClosedBars = 1
StopBufferPoints = 0
```

For buy:

```text
SL = min(real low, HA low) of closed signal candle
TP = entry + RewardR * (entry - SL)
```

For sell:

```text
SL = max(real high, HA high) of closed signal candle
TP = entry - RewardR * (SL - entry)
```

---

## Default Trade Limit

```text
MaxOpenTrades = 1
```

This keeps the first version clean and controlled.

---

## MQL5 Files

```text
mql5/Experts/Execution/E0010_PureHeikinAshiMtfRoulette.mq5
mql5/Include/Execution/DAL_ExecHeikinAshi.mqh
mql5/Include/Execution/DAL_ExecRouletteRisk.mqh
```

---

## Non-Goals

This module does not:

- use structural nodes,
- use M0001/M0002 regime labels,
- use Python,
- send pending orders,
- pyramid beyond the configured max-open-trade limit.
