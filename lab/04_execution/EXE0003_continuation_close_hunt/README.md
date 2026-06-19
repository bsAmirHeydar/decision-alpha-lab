# EXE0003 — Continuation Close-Hunt Market Execution

This lab contains the third H5 execution path:

- regime: continuation
- trigger: structural node close-hunt or Donchian 20 breakout
- entry: market on the next bar
- position size: cash risk to `3 × ATR` stop distance by default
- TP: none
- primary exit: regime change

Recommended first test:

```text
InpAtrPeriod = 14
InpAtrMultiplier = 3.0
InpEntryMode = E0003_ENTRY_DONCHIAN_BREAKOUT
InpDonchianPeriod = 20
InpUseLowerTimeframeRegimeFilter = true/false
InpCloseHuntBufferPoints = 0
InpMaxEntriesPerBar = 3
InpUseTradingSessionFilter = true/false according to the test window
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


## Build 1.03: Donchian 20 and optional lower-timeframe regime gate

Recommended Donchian-only continuation breakout test:

```text
InpEntryMode = E0003_ENTRY_DONCHIAN_BREAKOUT
InpDonchianPeriod = 20
InpUseLowerTimeframeRegimeFilter = false
InpUseHigherTimeframeRegimeFilter = true/false
InpUseAtrTrailingStop = true
InpExitOnRegimeChange = false
```

With the lower-timeframe regime filter off and regime exit off, E0003 can behave as a pure Donchian breakout + ATR trailing system: no TP, no local regime exit, and only the ATR trailing stop manages the open trade.
