# E0003 — H0005 Continuation Close-Hunt Market Executor

`E0003_ContinuationCloseHunt.mq5` is the third execution adapter for Decision Alpha Lab.
It is separate from `E0001` and `E0002`.

Build 1.03 adds an optional lower-timeframe regime gate and a Donchian breakout entry model.

## Contract

When the effective continuation gate passes:

1. The EA waits for a **closed candle**.
2. Entry can use either:
   - `E0003_ENTRY_CLOSE_HUNTED_NODE`: a structural node close-hunt.
   - `E0003_ENTRY_DONCHIAN_BREAKOUT`: Donchian breakout, default period 20.
3. Close-hunt model:
   - `HIGH` node close-hunt: `close > node.price + buffer` → buy continuation.
   - `LOW` node close-hunt: `close < node.price - buffer` → sell continuation.
4. Donchian model:
   - `close > highest(high, previous 20 closed candles) + buffer` → buy continuation.
   - `close < lowest(low, previous 20 closed candles) - buffer` → sell continuation.
5. The EA enters at market on the next bar.
6. There is no take-profit.
7. A technical SL is placed at `InpAtrMultiplier × ATR`, default `3 × ATR`.
8. Volume is sized from cash risk to the ATR stop distance.
9. Managed E0003 positions are closed when the effective continuation gate fails only if `InpExitOnRegimeChange=true`.

## Why the SL exists

The strategy exit is regime change. The ATR stop is used for risk sizing and catastrophic protection.
It is not the primary exit logic.

## Minimal inputs

- `InpSymbol`, `InpTimeframe`, `InpBars`
- `InpL`, `InpZoneRatio`, `InpExitGap`, `InpConsumeMode`
- `InpRegimeBasis`, `InpHumanContextSignal`
- `InpUseLowerTimeframeRegimeFilter`
- `InpEntryMode`, `InpDonchianPeriod`
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


## Build 1.03: lower-timeframe regime gate and Donchian entry

New inputs:

- `InpUseLowerTimeframeRegimeFilter`: when true, E0003 requires the local timeframe M0001/M0002 regime to be `CONTINUATION` before entering. When false, the local timeframe regime gate is skipped. If the higher-timeframe regime filter is also off, Donchian entries can trade directly from price breakout conditions.
- `InpEntryMode`: selects the trigger model. `E0003_ENTRY_DONCHIAN_BREAKOUT` is the new default; `E0003_ENTRY_CLOSE_HUNTED_NODE` keeps the original node close-hunt behavior.
- `InpDonchianPeriod`: Donchian lookback length, default `20`. The signal candle is excluded from the channel; the EA compares the latest closed candle against the previous 20 closed candles.

The existing ATR stop, ATR trailing, and optional regime-change exit remain unchanged.
