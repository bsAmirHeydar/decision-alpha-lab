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
