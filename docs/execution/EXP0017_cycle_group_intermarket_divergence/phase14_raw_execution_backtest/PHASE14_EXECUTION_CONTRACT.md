# Phase 14 Execution Contract

## 1. Signal authority

The executor accepts only signals satisfying all of the following:

```text
status == CONFIRMED_TRADEABLE
trade_permission_preview == true
data_ready == true
signal_id is non-empty
```

Signal construction remains owned by `CCGC_ConfirmationField`, including the Hotfix011 dual-symbol raw-M1 freshness proof.

## 2. Closed-candle decision boundary

The engine evaluates a boundary once per newly closed confirmation candle. It never reads shift 0 as the confirmation candle.

For a confirmation close `T` and timeframe length `P`:

```text
confirmation candle interval = [T - P, T)
```

The candle provider requires exactly one bar whose open time equals `T - P`. Missing or ambiguous bars reject the plan.

## 3. Trade-symbol selection

```text
PROTECTED mode -> signal.clean_symbol
HUNTER mode    -> signal.hunter_symbol
```

The signal direction does not change when the selected leg changes:

- low-side divergence remains BUY;
- high-side divergence remains SELL.

## 4. Entry model

The implemented entry model is:

```text
CGX_ENTRY_MARKET_ON_CLOSED_CANDLE
```

The planned entry is the current Ask for BUY and current Bid for SELL on the selected trade symbol. The quote is validated for spread, age, point size, and symbol availability.

Future entry types are isolated behind `CCGX_EntryModel`; they must not be added inside the signal source, stop model, or router.

## 5. Stop model

The implemented stop model is:

```text
CGX_STOP_BEHIND_CONFIRMATION_CANDLE
```

```text
BUY  SL = confirmation_candle_low  - stop_buffer_points * point
SELL SL = confirmation_candle_high + stop_buffer_points * point
```

Default buffer is zero. The planner rejects invalid direction geometry and broker stop-level violations rather than silently moving the stop.

## 6. Target model

The implemented target model is:

```text
CGX_TARGET_ATR_MULTIPLE
```

ATR is calculated from closed bars only using Wilder smoothing. The target is measured from the planned market entry:

```text
BUY  TP = entry + ATR * multiplier
SELL TP = entry - ATR * multiplier
```

Defaults:

```text
ATR period     = 14
ATR multiplier = 1.0
```

## 7. Volume models

Two isolated volume models are available:

1. Risk-percent equity, default 1%.
2. Fixed lots, default value 0.10 when selected.

Risk-percent sizing first uses `OrderCalcProfit` for one lot between entry and stop. If unavailable, it falls back to broker tick size and loss tick value.

The resulting volume is normalized downward to the broker volume step. By default, a risk-sized volume below broker minimum is rejected rather than rounded up beyond approved risk.

## 8. Duplicate and restart behavior

A signal ID is attempted at most once per trading day. The attempt is registered before planning/routing so a failed transport cannot be retried on a later candle and become a late entry.

On startup, the engine replays closed confirmation boundaries from the current New York trading-day start without sending orders. This reconstructs protected-reference lifecycle state and registers signals that already occurred before startup.

Warmup waits for M1 bounds on both configured symbols. The non-host symbol cannot be silently omitted.

## 9. Position-account behavior

`CGX_POSITION_EVERY_SIGNAL` is the default position policy.

A hedging account is the accurate environment for independent simultaneous signal positions. On a netting account, the explicit netting policy determines whether a new signal is skipped while a symbol position exists or allowed to merge into the net position.

The default profile requires a hedging account so every signal can retain independent SL/TP geometry. The requirement can be disabled explicitly; then the selected netting policy applies. The default netting policy is fail-safe skip because merged SL/TP geometry cannot preserve independent per-signal outcomes.

## 10. Runtime safety

Default runtime:

```text
CGX_RUNTIME_BACKTEST_ONLY
```

This mode sends orders only when the program is running in Strategy Tester or optimization. Paper mode creates plans and audit rows without transport. Live mode requires an explicit input change.
