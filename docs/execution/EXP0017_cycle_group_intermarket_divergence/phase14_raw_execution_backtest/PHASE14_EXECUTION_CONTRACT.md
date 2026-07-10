# Phase 14 Execution Contract

## 1. Signal authority

The executor accepts only signals satisfying all of the following:

```text
status == CONFIRMED_TRADEABLE
trade_permission_preview == true
data_ready == true
signal_id is non-empty
```

Signal construction remains owned by `CCGC_ConfirmationField`. Phase 14 does not redefine freshness, hunt asymmetry, lifecycle, or CG membership.

## 2. Closed-candle decision boundary

The engine evaluates a boundary once per newly closed confirmation candle. It never reads shift 0 as the confirmation candle.

```text
confirmation candle interval = [T - P, T)
```

The candle provider requires exactly one bar whose open time equals `T - P`.

## 3. Trade-symbol selection

```text
PROTECTED mode -> signal.clean_symbol
HUNTER mode    -> signal.hunter_symbol
```

The signal direction does not change when the selected leg changes.

## 4. Entry model

The current entry model is `CGX_ENTRY_MARKET_ON_CLOSED_CANDLE`.

- BUY planned entry: current Ask.
- SELL planned entry: current Bid.
- Quote age, spread, symbol point, and symbol availability are validated before planning continues.

## 5. Stop model

The stop model is `CGX_STOP_BEHIND_CONFIRMATION_CANDLE`.

```text
BUY  SL = confirmation low  - buffer
SELL SL = confirmation high + buffer + spread
```

The sell-spread addition is controlled by `InpAddSpreadToSellStop` and defaults to enabled.

## 6. Target models

### ATR multiple

```text
BUY  TP = entry + ATR * multiplier
SELL TP = entry - ATR * multiplier
```

ATR uses closed bars and Wilder smoothing. Defaults are period 14 and multiplier 1.0.

### Stop-risk multiple

```text
target distance = abs(entry - stop) * risk_reward_multiple
```

`InpRiskRewardMultiple` is used only when `CGX_TARGET_RISK_MULTIPLE` is selected.

## 7. Volume and risk models

### Fixed monetary risk

Default model: `CGX_VOLUME_FIXED_RISK_MONEY`.

The configured amount is in account deposit currency. Volume is always normalized downward and must satisfy:

```text
projected stop loss <= configured risk budget
```

If broker minimum volume exceeds the budget, the plan is rejected. The fixed-money model never rounds upward through the risk ceiling.

### Risk-percent equity

The percentage model remains available. Minimum-volume overflow is permitted only when explicitly enabled.

### Fixed lots

Fixed lots remain available for controlled comparison.

## 8. Hedge behavior

`InpEnableHedging=true` is the default.

- Enabled: opposite EXP0017 positions may coexist when the account supports hedging.
- Disabled: an opposite owned position on the same symbol blocks the new trade.
- Same-direction stacking is separately controlled by `InpPositionPolicy`.
- Netting-account behavior remains explicit through `InpNettingPolicy`.

## 9. Duplicate and restart behavior

A signal ID is attempted at most once per trading day. Attempt registration occurs before planning and routing, preventing a failed order from becoming a late retry.

Startup warmup replays closed boundaries without sending historical orders and waits for both configured symbols.

## 10. Execution visuals

The optional execution visual layer draws only accepted paper or broker executions from enabled CGs.

It owns prefix `EXP0017_P14_` and does not modify signal state. Divergence prices are symbol-local. Entry, stop, and target levels are drawn only on the matching trade-symbol chart.

## 11. Runtime safety

Default runtime is `CGX_RUNTIME_BACKTEST_ONLY`. Paper mode creates accepted plans without transport. Live transport requires an explicit runtime change.
