# EXE0010 — Pure Heikin Ashi MTF Roulette

## Purpose

E0010 is a pure Heikin Ashi execution module.

It does not use structural nodes, M-regime labels, or continuation/reversal classifiers.

It trades only from:

- current-forming higher-timeframe Heikin Ashi close/open body direction;
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

## Heikin Ashi body direction

There is no dependency on chart candle color.

Direction is defined only by the Heikin Ashi body:

```text
HA up body   = ha_close > ha_open
HA down body = ha_close < ha_open
HA doji      = ha_close == ha_open
```

## Buy rule

Buy only when:

```text
current-forming M10 HA: ha_close > ha_open
previous closed M1 HA: ha_close < ha_open
last closed M1 HA: ha_close > ha_open
max open trades allows entry
```

## Sell rule

Sell only when:

```text
current-forming M10 HA: ha_close < ha_open
previous closed M1 HA: ha_close > ha_open
last closed M1 HA: ha_close < ha_open
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

## Corrected Roulette logic

Roulette has a locked balance, a base risk, and a floor.

At cycle start:

```text
locked_balance = current_balance
base_risk = locked_balance * risk_percent
floor_balance = locked_balance - base_risk
```

If balance drops but remains above the floor, risk stays at base risk.

If balance breaks below the floor, the base used for volume calculation re-locks downward at the current balance:

```text
locked_balance = current_balance
base_risk = current_balance * risk_percent
floor_balance = locked_balance - base_risk
```

If balance goes into profit above locked balance, risk may grow using:

```text
risk = max(base_risk, (current_balance - floor_balance) * save_profit_factor)
```

If profit was active and then balance drops, the cycle re-locks to the post-loss balance.

## Files

```text
mql5/Experts/Execution/E0010_PureHeikinAshiMtfRoulette.mq5
mql5/Include/Execution/DAL_ExecHeikinAshi.mqh
mql5/Include/Execution/DAL_ExecRouletteRisk.mqh
```
