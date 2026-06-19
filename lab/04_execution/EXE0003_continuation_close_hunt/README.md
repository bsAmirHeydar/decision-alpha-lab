# EXE0003 — Continuation Close-Hunt Market Execution

This lab contains the third H5 execution path:

- regime: continuation
- trigger: structural node hunted by candle close
- entry: market on the next bar
- position size: cash risk to `3 × ATR` stop distance by default
- TP: none
- primary exit: regime change

Recommended first test:

```text
InpAtrPeriod = 14
InpAtrMultiplier = 3.0
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

