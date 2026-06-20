# E0005 — Continuation Close-Break Fixed-R Executor

E0005 is the fifth H0005 execution module.

It is a separate Expert Advisor. It does not modify E0001, E0002, E0003, or E0004.

## Contract

E0005 trades only the continuation side of H0005.

A signal is valid when:

1. The local M0002 regime is continuation.
2. The latest fully closed candle breaks a confirmed structural node by close.
3. The node was active before the signal candle.
4. The same node was not already close-broken before the signal candle.
5. The node is not already consumed by a M0001 event.
6. Optional higher-timeframe regime filter passes.

## Direction

- Close above a confirmed HIGH node = bullish continuation = market buy.
- Close below a confirmed LOW node = bearish continuation = market sell.

## Risk and target

The stop distance is ATR-based.

Default:

```text
InpAtrPeriod = 14
InpAtrMultiplier = 4.0
```

So the stop distance is:

```text
SL distance = 4 × ATR(14)
```

The take-profit is fixed R.

Default:

```text
InpRewardR = 1.0
```

So the default target is 1:1 against the ATR stop distance.

Examples:

```text
InpAtrMultiplier = 4.0
InpRewardR = 1.0
```

means 4 ATR stop and 1R target.

```text
InpAtrMultiplier = 4.0
InpRewardR = 2.0
```

means 4 ATR stop and 2R target.

## No-future behavior

E0005 processes only on a new open candle and evaluates the last fully closed candle.

It loads closed bars only, removes the currently forming candle, and checks node `active_from_index` before accepting a signal. This keeps the execution aligned with live data availability.

## Higher-timeframe filter

```text
InpUseHigherTimeframeRegimeFilter = false
InpHigherRegimeTimeframe = PERIOD_H1
InpUseHigherTimeframeDirectionFilter = false
```

When the HTF filter is off, E0005 uses only the local timeframe regime.

When the HTF filter is on, the higher timeframe must have continuation energy.

When `InpUseHigherTimeframeDirectionFilter` is false, the higher timeframe only gives permission to trade and does not restrict buy/sell direction.

When it is true, the trade direction must match the latest higher-timeframe close-break direction.
