# EXE0011 — Donchian 20 ATR3 Roulette Execution

## Purpose

`E0011_Donchian20Atr3Roulette` is a pure MQL5 execution expert for a simple breakout continuation model:

- entry from a fresh Donchian 20 breakout
- stop-loss at 3 ATR
- take-profit at 2R
- money risk from the reusable Roulette risk module

No Python, no external execution scripts, and no structural-regime dependency are used.

---

## Default Inputs

```text
InpSignalTimeframe = PERIOD_M1
InpDonchianPeriod = 20
InpATRPeriod = 14
InpATRStopMultiplier = 3.0
InpRewardR = 2.0
InpMaxOpenTrades = 1
InpRouletteInitialRiskPercent = 10.0
InpRouletteSaveProfitFactor = 0.50
InpRoulettePersistState = true
```

---

## Execution Clock

The expert does not evaluate on every tick.

It evaluates once when a new `InpSignalTimeframe` candle opens. Therefore the signal candle is always the last closed candle, `shift 1`.

---

## Donchian Breakout Rule

The Donchian channel is calculated causally.

For a period of 20:

- signal candle = `shift 1`
- Donchian range for the signal = highs/lows of `shift 2` through `shift 21`
- previous candle = `shift 2`
- previous Donchian range = highs/lows of `shift 3` through `shift 22`

### Buy

```text
signal_close > upper_20
previous_close <= previous_upper_20
```

This means the last closed candle freshly broke above the previous 20-candle Donchian upper band.

### Sell

```text
signal_close < lower_20
previous_close >= previous_lower_20
```

This means the last closed candle freshly broke below the previous 20-candle Donchian lower band.

---

## Stop-Loss

The stop is based on ATR from the last closed signal-timeframe candle.

```text
ATR = ATR(InpATRPeriod, shift 1)
stop_distance = ATR * InpATRStopMultiplier
```

Default:

```text
stop_distance = ATR(14, shift 1) * 3.0
```

### Buy Stop

```text
SL = entry_price - 3 * ATR
```

### Sell Stop

```text
SL = entry_price + 3 * ATR
```

---

## Take-Profit

Take-profit is fixed at 2R by default.

### Buy

```text
TP = entry_price + 2 * (entry_price - SL)
```

### Sell

```text
TP = entry_price - 2 * (SL - entry_price)
```

---

## Roulette Risk

The expert asks `DAL_ExecRouletteRisk.mqh` for money risk.

Roulette logic:

- lock current balance at cycle start
- calculate base risk from locked balance
- keep base risk fixed while balance remains inside the drawdown band
- if balance breaks below the protected floor, re-lock downward at current balance
- if a profit cluster forms, risk can expand using `save_profit_factor`
- after a profit cluster, the first realized loss re-locks the cycle at the post-loss balance

The execution expert converts returned money risk into lots using the stop distance and symbol tick value.

---

## Safety

The expert:

- uses only closed candles for Donchian signals
- does not include the signal candle inside its own Donchian channel
- does not trade if stop distance is invalid
- does not trade if calculated volume would violate the risk budget unless explicitly allowed by input
- defaults to one open managed trade
