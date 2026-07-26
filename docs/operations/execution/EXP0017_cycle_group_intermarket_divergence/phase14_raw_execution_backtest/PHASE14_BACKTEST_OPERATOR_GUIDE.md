# Phase 14 Backtest Operator Guide

## Compile target

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Raw_Execution_Backtest.mq5
```

## Default test profile

```text
Host symbol: SPXUSD
Confirmation timeframe: chart timeframe
Trade leg: protected symbol
Entry: market on first tick after closed candle
Stop: behind confirmation candle
Sell spread adjustment: enabled
Target model: ATR multiple
ATR period: 14
ATR multiplier: 1.0
Volume model: fixed monetary risk
Fixed risk: 100 account-currency units
Hedging: enabled
Execution visuals: enabled
cg_3m: enabled
all other CGs: disabled
one-shot divergence execution: hard enabled
```

For a USD test account, `InpFixedRiskMoney=100` means a planned maximum stop loss of USD 100 before commission, gaps, and execution slippage.

## Alternative target test

Select:

```text
InpTargetModel = CGX_TARGET_RISK_MULTIPLE
InpRiskRewardMultiple = 1.0
```

The TP distance then equals one confirmation-stop distance.

## Hedge-off test

Set `InpEnableHedging=false` and generate an opposite signal while an EXP0017 position remains open on the same symbol. The second trade must be rejected with:

```text
hedging_disabled_opposite_position_exists
```

## Visual test

Run Strategy Tester in visual mode.

- Executed CG divergence legs use prefix `EXP0017_P14_`.
- The selected trade-symbol chart receives entry, stop, and TP segments.
- No drawing should appear for rejected plans.
- Disable all execution drawings with `InpDrawExecutedCGSignals=false`.

## Audit output

Default file:

```text
EXP0017_Phase14_Raw_Execution_Audit_V3.csv
```

The audit includes target model, volume model, hedge state, spread, stop distance, risk budget, one-lot risk, projected stop loss, normalized volume, and broker result.

## One-shot test

Use a visual case where the same divergence remains confirmed across multiple lower-timeframe candle closes. The first observation may create one trade opportunity. Every later observation must be suppressed even after a planning or broker failure.

The main execution audit includes `trade_entitlement_key`. Duplicate observations are written to:

```text
EXP0017_Phase14_Raw_Execution_Audit_V3_OneShot_Gate.csv
```

Group by `trade_entitlement_key`; accepted execution count must never exceed one. See [[PHASE14_ONE_SHOT_VALIDATION_PLAN]].
