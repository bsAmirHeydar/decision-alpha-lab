# 08 - Open Questions Before Implementation

This strategy should not be coded until these decisions are locked.

## Critical questions

### Q1 - W comparison matrix direction

The source says current W is compared only with previous W cycles in the same M, but the printed matrix can be interpreted ambiguously:

```text
W2 <- W1
W1 or W3 <- W2
W1 or W2 or W4 <- W3
```

Decision needed:

- Use previous-only matrix?
- Use literal SRS matrix?
- Add input mode and test both?

Recommended:

```text
InpReferenceMatrixMode = PREVIOUS_ONLY / SRS_LITERAL / CUSTOM
```

### Q2 - Gap behavior

What should the EA do during:

```text
02:00 -> 03:00
09:00 -> 09:30
```

Options:

1. No detection, only manage positions.
2. Allow pending confirmations only.
3. Treat gaps as dead zones and cancel pending divergences.

### Q3 - Check candle alignment

If raw divergence appears in the middle of a check candle, should the EA wait for:

1. the currently forming check candle to close;
2. the next full check candle to close?

Recommended:

- Wait for the currently active check-candle close if the divergence forms before that close.

### Q4 - TP formula

The SRS says TP uses Final Reward, but does not explicitly define formula.

Recommended candidate:

```text
TP = entry +/- FinalReward * abs(entry - SL)
```

Confirm whether `Final Reward = 10` means `10R`.

### Q5 - Position size formula

Recommended candidate:

```text
volume = (equity * risk_percent / 100) / (stop_distance_points * contract_size)
```

Confirm whether this matches the author's intended contract-size usage.

### Q6 - Execution price

Entry is "immediate after check candle close".

Implementation options:

1. market order on the next tick after close;
2. open price of the next bar in backtest;
3. close price of confirmation candle in research reports.

Recommended:

- Live: market order after check candle close.
- Backtest: next bar open, with optional slippage.

### Q7 - Touch equality

For hunt, should equality count?

Recommended:

```text
Low hunt: low <= level
High hunt: high >= level
```

### Q8 - Multiple reference W hits in same event

If one symbol hunts several eligible W levels at the same time, source says closest W by time is selected for stop-loss.

Confirm whether the divergence ID should use:

- only closest W;
- all hunted W references but choose closest W for SL.

### Q9 - Partial close rounding

The source gives examples:

```text
1.01 -> close 0.51
0.01 -> close full
```

Need general rounding policy for broker volume step.

### Q10 - Live-order safety

The SRS allows extremely large calculated volume with no cap.

For real live trading, should we add an optional safety kill-switch outside the strategy contract?

Recommended:

```text
InpMaxLiveVolumeSafety = 0 means disabled
```

Keep disabled by default if strict SRS behavior is required.

## Non-blocking enhancements

- Optional audit chart drawing.
- Optional report-only mode.
- Optional custom symbol mapping for CME ES/NQ to broker SPX/NDX execution.
- Optional CSV bridge support from `EXP0015` data-source layer.

