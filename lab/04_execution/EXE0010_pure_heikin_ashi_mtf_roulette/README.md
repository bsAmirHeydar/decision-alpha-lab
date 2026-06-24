# EXE0010 — Pure Heikin Ashi MTF Roulette

## Purpose

E0010 is a pure Heikin Ashi execution module.

It does not use structural nodes, M-regime labels, or continuation/reversal classifiers.

It trades only from:

- current-forming higher-timeframe Heikin Ashi direction;
- completed lower-timeframe Heikin Ashi close/open body direction flip;
- Roulette risk sizing.

## Timeframes

Default:

```text
Entry timeframe = PERIOD_M1
Direction timeframe = PERIOD_M10
```

The M10 candle is intentionally the **current-forming** Heikin Ashi candle.

The M1 trigger is intentionally based only on **closed** candles.

## Execution clock

The EA does not evaluate entry logic on every tick.

It runs the execution decision only once when a new lower-timeframe bar opens.

This means the previous M1 candle has just closed, and only that completed candle is allowed to trigger.

## Buy rule

Buy only when:

```text
current-forming M10 HA = HA close above HA open
previous closed M1 HA = HA close below HA open
last closed M1 HA = HA close above HA open
max open trades allows entry
```

## Sell rule

Sell only when:

```text
current-forming M10 HA = HA close below HA open
previous closed M1 HA = HA close above HA open
last closed M1 HA = HA close below HA open
max open trades allows entry
```

## Risk and target

Default:

```text
MaxOpenTrades = 1
RewardR = 2.0
RouletteInitialRiskPercent = 10.0
RouletteSaveProfitFactor = 0.50
```

TP is 1:2 by default.

Stop is derived from the closed lower-timeframe signal candle using real candle and Heikin Ashi extremes.

For buy:

```text
SL = min(real low, HA low)
TP = entry + 2R
```

For sell:

```text
SL = max(real high, HA high)
TP = entry - 2R
```

## Roulette logic

Roulette keeps base risk fixed while losing below the initial floor.

It grows only after the account becomes profitable relative to the locked balance.

After profit then loss, it resets the locked balance to the balance after loss.

Consecutive losses after reset keep the new base risk fixed.

## Files

```text
mql5/Experts/Execution/E0010_PureHeikinAshiMtfRoulette.mq5
mql5/Include/Execution/DAL_ExecHeikinAshi.mqh
mql5/Include/Execution/DAL_ExecRouletteRisk.mqh
```
