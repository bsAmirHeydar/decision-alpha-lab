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
