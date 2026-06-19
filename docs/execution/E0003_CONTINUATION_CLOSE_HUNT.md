# E0003 — H0005 Continuation Close-Hunt Market Executor

`E0003_ContinuationCloseHunt.mq5` is the third execution adapter for Decision Alpha Lab.
It is separate from `E0001` and `E0002`.

## Contract

When the effective regime is `CONTINUATION`:

1. The EA waits for a **closed candle**.
2. If that candle closes through a structural node, the node is considered close-hunted:
   - `HIGH` node close-hunt: `close > node.price + buffer` → buy continuation.
   - `LOW` node close-hunt: `close < node.price - buffer` → sell continuation.
3. The EA enters at market on the next bar.
4. There is no take-profit.
5. A technical SL is placed at `InpAtrMultiplier × ATR`, default `3 × ATR`.
6. Volume is sized from cash risk to the ATR stop distance.
7. All managed E0003 positions are closed when the effective regime is no longer continuation.

## Why the SL exists

The strategy exit is regime change. The ATR stop is used for risk sizing and catastrophic protection.
It is not the primary exit logic.

## Minimal inputs

- `InpSymbol`, `InpTimeframe`, `InpBars`
- `InpL`, `InpZoneRatio`, `InpExitGap`, `InpConsumeMode`
- `InpRegimeBasis`, `InpHumanContextSignal`
- trading session start/end
- `InpMagicNumber`, `InpRiskCash`
- `InpAtrPeriod`, `InpAtrMultiplier`
- `InpCloseHuntBufferPoints`, `InpMaxEntriesPerBar`

## Logs

Entry log:

```text
DAL_E0003_CONTINUATION_ENTRY
```

Regime-change exit log:

```text
DAL_E0003_REGIME_EXIT_CLOSE
```

## Higher-timeframe regime filter

All four execution experts now support an optional higher-timeframe regime gate. The default is off, so existing tests are unchanged.

Inputs:

- `InpUseHigherTimeframeRegimeFilter` — enable/disable the higher-timeframe regime confirmation.
- `InpHigherRegimeTimeframe` — timeframe used for the higher-timeframe M0001/M0002 regime calculation, default `PERIOD_H1`.

Behavior:

- E0001 and E0002 require the higher timeframe to be `REVERSAL` before allowing reversal entries.
- E0003 and E0004 require the higher timeframe to be `CONTINUATION` before allowing continuation entries.
- The higher-timeframe filter is a gate only; it does not change node construction, touch locking, TP policy, or trade management.



## Build 1.02: ATR trailing and optional regime exit

E0003 now supports two additional execution controls:

- `InpUseAtrTrailingStop`: when enabled, every new closed candle trails the SL by `InpAtrMultiplier × ATR`. Buy stops only move upward to `close - 3ATR`; sell stops only move downward to `close + 3ATR`.
- `InpExitOnRegimeChange`: when enabled, E0003 closes its managed positions when the effective regime is no longer continuation. When disabled, open positions are not closed by regime change and can be managed only by the ATR trailing stop.

There is still no take-profit in E0003.
