# Intermarket Divergence Experts

## IMD001_SPX_NDX_TimeDivergence

Batch expert for EXP0015. It scans two aligned symbols, usually S&P/US500 and Nasdaq/NAS100, and records time-step divergences between their highs/lows.

The expert is intentionally not tick-driven. `OnTick()` is empty. In research mode the whole scan runs once in `OnInit()` and exports CSV files to Common Files.

Default output:

```text
Common\Files\imd\EXP0015\imd001_divergence_events.csv
Common\Files\imd\EXP0015\imd001_summary.csv
```

Turn on `InpWriteAllEvaluatedSteps` only when you need a full audit table for every compared high/low step. It can be large.
