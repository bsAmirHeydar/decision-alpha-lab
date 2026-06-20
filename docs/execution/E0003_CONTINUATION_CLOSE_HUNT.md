# E0003 — H0005 Continuation Close-Hunt Market Executor

`E0003_ContinuationCloseHunt.mq5` is the third execution adapter for Decision Alpha Lab.
It is separate from `E0001` and `E0002`.

Build 1.06 adds a selectable Donchian trigger policy: immediate intrabar tick breakout or closed-bar confirmation.

## Contract

When the effective continuation gate passes:

1. The EA waits for a **closed candle**.
2. Entry can use either:
   - `E0003_ENTRY_CLOSE_HUNTED_NODE`: a structural node close-hunt.
   - `E0003_ENTRY_DONCHIAN_BREAKOUT`: Donchian breakout, default period 20, with selectable trigger policy.
3. Close-hunt model:
   - `HIGH` node close-hunt: `close > node.price + buffer` → buy continuation.
   - `LOW` node close-hunt: `close < node.price - buffer` → sell continuation.
4. Donchian model:
   - The channel is built from the previous 20 **closed** candles.
   - `InpDonchianTriggerMode=E0003_DONCHIAN_TRIGGER_INTRABAR_TICK`: `Ask > upper + buffer` buys immediately; `Bid < lower - buffer` sells immediately.
   - `InpDonchianTriggerMode=E0003_DONCHIAN_TRIGGER_CLOSED_BAR`: the latest closed candle must close beyond the channel; entry is sent on the next processing pass.
5. Close-hunt node mode enters on the next bar. Donchian mode follows the selected trigger policy.
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
- `InpEntryMode`, `InpDonchianTriggerMode`, `InpDonchianPeriod`
- trading session start/end
- `InpMagicNumber`, `InpRiskCash`
- `InpAtrPeriod`, `InpAtrMultiplier`
- `InpCloseHuntBufferPoints`, `InpMaxEntriesPerBar`, `InpMaxSimultaneousTrades`

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
- `InpUseHigherTimeframeDirectionFilter` — when false, the higher timeframe only grants/blocks continuation permission; it does not restrict buy/sell direction. When true, the signal direction must match the latest higher-timeframe close-hunt direction.

Behavior:

- E0001 and E0002 require the higher timeframe to be `REVERSAL` before allowing reversal entries.
- E0003 and E0004 require the higher timeframe to be `CONTINUATION` before allowing continuation entries.
- For E0003, direction filtering is optional. With `InpUseHigherTimeframeDirectionFilter=false`, HTF continuation is only a permission gate and Donchian/node signals may trade either direction. With it enabled, buy signals require bullish HTF close-hunt direction and sell signals require bearish HTF close-hunt direction.
- The higher-timeframe filter is a gate only; it does not change node construction, touch locking, TP policy, SL policy, trailing, or trade management.



## Build 1.02: ATR trailing and optional regime exit

E0003 now supports two additional execution controls:

- `InpUseAtrTrailingStop`: when enabled, every new closed candle trails the SL by `InpAtrMultiplier × ATR`. Buy stops only move upward to `close - 3ATR`; sell stops only move downward to `close + 3ATR`.
- `InpExitOnRegimeChange`: when enabled, E0003 closes its managed positions when the effective regime is no longer continuation. When disabled, open positions are not closed by regime change and can be managed only by the ATR trailing stop.

There is still no take-profit in E0003.


## Build 1.03: lower-timeframe regime gate and Donchian entry

New inputs:

- `InpUseLowerTimeframeRegimeFilter`: when true, E0003 requires the local timeframe M0001/M0002 regime to be `CONTINUATION` before entering. When false, the local timeframe regime gate is skipped. If the higher-timeframe regime filter is also off, Donchian entries can trade directly from price breakout conditions.
- `InpEntryMode`: selects the trigger model. `E0003_ENTRY_DONCHIAN_BREAKOUT` is the new default; `E0003_ENTRY_CLOSE_HUNTED_NODE` keeps the original node close-hunt behavior.
- `InpDonchianPeriod`: Donchian lookback length, default `20`. The current candle is excluded from the channel. The EA builds the channel from the previous 20 closed candles, but the trigger is intrabar: the first tick whose Ask/Bid breaks the channel can send a market order immediately.

The existing ATR stop, ATR trailing, and optional regime-change exit remain unchanged.


## Build 1.04: max trades and HTF direction control

New inputs:

- `InpMaxSimultaneousTrades`: maximum number of simultaneously open E0003 managed positions. Use `-1` for unlimited. Use `1` for one position at a time.
- `InpUseHigherTimeframeDirectionFilter`: keeps the higher-timeframe regime filter from over-constraining direction by default.

Default behavior:

```text
InpUseHigherTimeframeRegimeFilter = false
InpUseHigherTimeframeDirectionFilter = false
InpMaxSimultaneousTrades = -1
```

If the HTF regime filter is enabled and direction filter is false, the higher timeframe only says whether continuation energy exists. It does not force the EA to buy-only or sell-only. If direction filter is true, the EA also requires the entry direction to match the latest higher-timeframe close-hunt direction.


## Build 1.05: intrabar Donchian market trigger

Donchian mode no longer waits for candle close confirmation. The Donchian channel is still calculated from the previous `InpDonchianPeriod` closed candles, but entry is triggered on the live tick:

```text
Buy  = Ask > previous Donchian upper + buffer
Sell = Bid < previous Donchian lower - buffer
```

The EA allows at most one Donchian buy and one Donchian sell trigger per current candle, then `InpMaxSimultaneousTrades` controls whether the order can actually be opened. ATR stop, ATR trailing, lower-timeframe regime gate, higher-timeframe permission/direction gate, and optional regime-change exit remain unchanged.


## Build 1.06: selectable Donchian trigger policy

New input:

- `InpDonchianTriggerMode`

Available values:

```text
E0003_DONCHIAN_TRIGGER_INTRABAR_TICK
E0003_DONCHIAN_TRIGGER_CLOSED_BAR
```

`E0003_DONCHIAN_TRIGGER_INTRABAR_TICK` keeps the previous 1.05 behavior: the channel is calculated from the previous `InpDonchianPeriod` closed candles, but the EA enters immediately when the live Ask/Bid breaks the channel.

`E0003_DONCHIAN_TRIGGER_CLOSED_BAR` waits for the latest fully closed candle to close outside the previous Donchian channel. The signal candle itself is excluded from the channel; the entry is sent only after that candle is closed.

The default remains intrabar tick breakout to preserve the latest execution behavior. ATR stop, ATR trailing, lower-timeframe regime gate, higher-timeframe permission/direction gate, max simultaneous trades, and optional regime-change exit remain unchanged.
