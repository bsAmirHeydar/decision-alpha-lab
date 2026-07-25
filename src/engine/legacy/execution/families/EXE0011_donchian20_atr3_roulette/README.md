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

---

## Two-Layer Micro-Probe Profit Gate

E0011 supports an optional two-layer execution filter.

The goal is:

```text
first winning signal opens permission for the next full trades
full winning trades keep permission open
first full losing or flat trade closes permission
while permission is closed, only micro-probe trades are taken
first profitable micro-probe opens permission again
```

This replaces a purely virtual shadow stream with real micro-lot probe orders.

The reason is practical: using micro-probe orders keeps the system compatible with real broker/tester mechanics, including `InpMaxOpenTrades = 1`. A blocked signal still creates a tiny real position, so the EA naturally waits until that probe position is closed before considering the next signal.

Default inputs:

```text
InpHypoGateEnabled = true
InpHypoGateStartOpen = false
InpHypoGatePersistState = true
InpHypoGateProbeVolume = 0.01
```

---

## Layer 1 — Blocked Micro-Probe Layer

When the gate is closed, valid Donchian breakout signals are not ignored.

They are sent as tiny probe orders, default `0.01` lot, using the exact same execution plan:

```text
same direction
same market entry logic
same ATR stop
same 2R target
same broker SL/TP mechanics
```

A probe order is identified by the comment layer marker:

```text
E0011DONP...
```

Probe result controls only the gate:

```text
probe profit > 0  => open the gate for the NEXT full signal
probe profit <= 0 => keep the gate closed
```

Probe trades do not update Roulette.

They are real orders for gating/backtest-mechanics only, not part of the Roulette-sized production stream.

---

## Layer 2 — Full Live Roulette Layer

When the gate is open, valid Donchian breakout signals are executed as full live trades sized by Roulette.

A full live order is identified by the comment layer marker:

```text
E0011DONL...
```

Full live result controls both the gate and Roulette:

```text
full trade profit > 0  => keep gate open and update Roulette
full trade profit <= 0 => close gate and update Roulette
```

After a full losing or flat trade, the EA stops taking full Roulette-sized trades.

It then goes back to the micro-probe layer and waits until a probe order wins.

---

## Final Gate Sequence

The intended sequence is:

```text
Gate closed
-> valid signal is executed as 0.01 probe
-> if probe loses, keep taking only 0.01 probes
-> if probe wins, gate opens
-> next valid signal is full Roulette-sized
-> if full trade wins, continue full Roulette-sized trades
-> if full trade loses, gate closes
-> return to 0.01 probe mode
```

Important: the winning probe itself does not become a full trade retroactively. It only opens permission for the next signal.

---

## Roulette Scope

Roulette applies only to full live trades.

```text
probe 0.01 trade closed => update gate only, do not update Roulette
full Roulette trade closed => update gate and update Roulette
```

This keeps Roulette attached to the real production trade stream, while the micro-probe stream remains a permission filter.
