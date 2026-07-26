# Phase 14 Execution Controls V2

## Scope

This patch extends the raw backtest executor without changing EXP0017 divergence detection, reference freshness, lifecycle, CG definitions, or closed-candle confirmation.

## Hedge switch

`InpEnableHedging` defaults to `true`.

- When enabled, opposite-direction EXP0017 positions may coexist on a hedging account.
- When disabled, the router rejects a new EXP0017 order if an owned opposite-direction position already exists on the same symbol.
- Same-direction stacking remains controlled by `InpPositionPolicy`.
- `InpRequireHedgingAccount` applies only while hedging is enabled.

## Stop geometry

The stop remains behind the selected trade symbol's closed confirmation candle.

```text
BUY  SL = candle low  - point buffer
SELL SL = candle high + point buffer + current spread
```

`InpAddSpreadToSellStop` defaults to `true`. The spread used by the stop model is the same validated quote spread used by the entry planner.

## Target models

Two target providers are available:

```text
CGX_TARGET_ATR_MULTIPLE
CGX_TARGET_RISK_MULTIPLE
```

ATR mode remains the default. `InpATRMultiplier` is independently editable.

Risk-multiple mode calculates:

```text
stop distance   = abs(entry - stop)
target distance = stop distance * InpRiskRewardMultiple
```

## Fixed-money risk sizing

`CGX_VOLUME_FIXED_RISK_MONEY` is the new default volume model.

`InpFixedRiskMoney` is interpreted in account deposit currency. On a USD account, the value is a dollar-risk cap.

The volume model:

1. calculates one-lot stop loss through `OrderCalcProfit`, with broker tick-value fallback;
2. divides the configured risk budget by one-lot loss;
3. caps at broker maximum volume;
4. rounds volume downward to broker step;
5. verifies projected stop loss does not exceed the configured budget;
6. rejects the trade when broker minimum volume would exceed the budget.

The selected result is the largest broker-valid volume that remains at or below the configured planned stop-loss budget.

## Execution visuals

`InpDrawExecutedCGSignals` defaults to `true`.

Only accepted executions are drawn. A signal rejected by planning, position policy, or broker transport is not rendered as an executed trade.

The visual module owns the `EXP0017_P14_` object prefix and can draw:

- the symbol-local divergence leg for the enabled/traded CG;
- entry, stop, and target levels on the matching trade-symbol chart.

The visual layer does not generate signals or alter order geometry.

## Interaction with one-shot execution

Hedging, position stacking, ATR/R targets, fixed-money sizing, spread-aware stops, and visuals do not create additional permission for a persistent divergence. They operate only after the mandatory one-shot entitlement has been consumed. See [[PHASE14_ONE_SHOT_SIGNAL_EXECUTION_CONTRACT]].
