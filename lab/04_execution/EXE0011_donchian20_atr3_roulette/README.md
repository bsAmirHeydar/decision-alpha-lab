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

## Two-Layer Hypothetical Profit Gate

E0011 also supports an optional two-layer execution filter.

The goal is to avoid trading immediately after a losing trade until the same signal stream proves itself again with a hypothetical win.

Default inputs:

```text
InpHypoGateEnabled = true
InpHypoGateStartOpen = false
InpHypoGatePersistState = true
```

### Layer 1 — Hypothetical Layer

When the gate is closed, valid Donchian breakout signals are not sent to the broker.

Instead, the first valid signal is opened as a hypothetical trade using the same execution plan:

```text
same direction
same entry reference
same ATR stop
same 2R target
```

This virtual trade is tracked on every tick.

For a buy virtual trade:

```text
win  = Bid >= virtual_take_profit
loss = Bid <= virtual_stop
```

For a sell virtual trade:

```text
win  = Ask <= virtual_take_profit
loss = Ask >= virtual_stop
```

If the virtual trade wins, the real execution gate opens.

The winning virtual trade itself is not executed retroactively. Only the next valid signals are allowed live.

If the virtual trade loses, the gate stays closed and the system waits for the next valid hypothetical trade to win.

### Layer 2 — Real Execution Layer

When the gate is open, valid Donchian breakout signals are executed live.

Real closed trade result controls the gate:

```text
real trade profit > 0  => keep gate open
real trade profit <= 0 => close gate and wait for a hypothetical win again
```

So the sequence is:

```text
blocked -> hypothetical signal -> hypothetical win -> real signals allowed
real win -> continue taking real signals
real loss -> block again -> wait for hypothetical win
```

This means the EA has two different streams:

```text
Hypothetical stream: used only to re-open permission after loss
Real stream: used only while permission is open
```

The gate does not change Donchian logic, ATR stop logic, Roulette risk, lot sizing, or order sending. It only decides whether a valid signal is allowed to reach the real execution layer.


## Roulette Live-Only Rule

Roulette is applied only to trades that are actually executed by E0011.

The hypothetical layer does not change Roulette state. A shadow trade can open the gate or keep it closed, but it never changes `locked_balance`, `base_risk`, `floor_balance`, `profit_active`, or the next real lot size.

Operationally:

```text
Gate closed + valid signal:
  -> create/update hypothetical trade only
  -> do not call Roulette risk sizing
  -> do not update Roulette state

Gate open + valid signal:
  -> call RouletteRiskMoney()
  -> calculate real volume
  -> send real order

Real managed trade closes:
  -> update hypothetical gate from real P/L
  -> update Roulette from actual account balance
```

This means Roulette follows only the real executed trade stream, not the shadow stream.
