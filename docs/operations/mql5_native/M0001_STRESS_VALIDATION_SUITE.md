# M0001 Stress Validation Suite

Version: 1.61

This document locks the additional validation layer around M0001. The structural-node, territory, touch/HUNT, revisit, RTV, logRTV, warmup, analysis-start, and final visual semantics are unchanged. Version 1.61 adds final-only stress reports that try to break the node-vs-random volatility-expansion fact under harder nulls.

## Runtime principle

The EA remains candle-gated and final-only by default:

```text
intra-candle ticks -> return immediately
new candle -> append the previous closed candle once
OnDeinit -> compute the final node/event/audit state once
OnDeinit -> print validation and stress reports
OnDeinit -> draw final visuals once, if enabled
```

No stress test changes the event definition. Stress tests operate after the final event set is built.

## New inputs

```text
InpRunStressSuite = true
InpBrokerUtcOffsetHours = 0
InpRegimeLookbackBars = 100
InpHardRandomCandidates = 80
InpPlaceboShiftBars = 50
InpNonOverlapGapBars = 0
InpBlockBootstrapIterations = 300
InpBlockBootstrapBlockPairs = 25
InpHorizonBars1 = 5
InpHorizonBars2 = 10
InpHorizonBars3 = 20
InpHorizonBars4 = 50
```

`InpBrokerUtcOffsetHours` converts broker-server hour to UTC hour for session reports. If broker time is UTC+2, set it to `2`. If broker time is UTC+3, set it to `3`.

`InpRegimeLookbackBars` defines the pre-entry realized-volatility regime:

```text
preEntryVol = mean(abs(log(high / low))) over N bars before event entry
```

Regimes are terciles of this pre-entry value. This replaces the older diagnostic `randomLogTercile` regime and is live-safe because it only uses information before event entry.

## Final stress reports

### HARD_NULL

Printed as:

```text
DAL_M0001_FINAL_STRESS_NULLS ... HARD_NULL
```

For every node event, the test tries to find random windows that match:

```text
same sample length
same UTC session
same pre-entry volatility tercile
same pre-entry trend regime on the first pass
```

If no candidate passes the trend condition, it falls back to session + pre-vol tercile. This is deliberately harder than simple random sampling.

### PLACEBO

Printed as:

```text
DAL_M0001_FINAL_PLACEBO ... PLACEBO
```

The test shifts each real event entry by `+InpPlaceboShiftBars` and `-InpPlaceboShiftBars`, keeps the same sample length, and compares the shifted windows against the original random baseline. Real nodes should outperform shifted placebo timing.

### OUTLIER_STRESS

Printed as:

```text
DAL_M0001_FINAL_OUTLIER_STRESS ... OUTLIER_STRESS
```

Includes:

```text
fullMean
removeTop1Mean
removeTop5Mean
winsor1Mean
winsor5Mean
medianOfMeans10
```

This tests whether the edge survives after the strongest tail outcomes are removed or capped.

### NONOVERLAP

Printed as:

```text
DAL_M0001_FINAL_NONOVERLAP ... NONOVERLAP
```

The event list is sorted chronologically and overlapping event windows are removed. This reduces dependence between nearby events.

### CLUSTER_ROBUST

Printed as:

```text
DAL_M0001_FINAL_CLUSTER_ROBUST ... CLUSTER_ROBUST
```

Computes t-style diagnostics on daily and weekly cluster means. This is stricter than treating every event as independent.

### BLOCK_BOOT

Printed as:

```text
DAL_M0001_FINAL_BLOCK_BOOT ... BLOCK_BOOT
```

Uses contiguous blocks of paired deltas to build a CI that is more robust to autocorrelation and volatility clustering than single-event bootstrap.

### HORIZON

Printed as:

```text
DAL_M0001_FINAL_HORIZON ... HORIZON
```

Tests fixed future horizons, independent of the event exit-gap RTV window:

```text
h5, h10, h20, h50 by default
```

For each horizon, it compares node-entry horizon RTV against a deterministic random horizon window. This helps estimate timing, decay, and approximate half-life.

### NEGATIVE_CONTROL

Printed as:

```text
DAL_M0001_FINAL_NEGATIVE_CONTROL ... NEG_CONTROL_RANDOM_VS_RANDOM
```

Compares two independent random windows of the same length. The expected mean should be close to zero. If this control is also strongly positive, the null engine itself may be biased.

## Existing reports now corrected

`DAL_M0001_FINAL_SESSION_REGIME` now uses:

```text
sessionClock=UTC
regimeBy=preEntryVolTercile
trendBy=preEntryCloseReturn
```

This removes the previous broker-hour and random-outcome dependency.

## Batch-level tests

Some robustness tests cannot be computed inside one single-symbol/single-timeframe EA run:

```text
leave-one-market-out
leave-one-timeframe-out
cross-market meta-analysis
multiple-testing correction across a full grid of runs
```

For these, export/copy the final Journal lines from multiple runs and use:

```text
tools/m0001_report_meta_aggregate.py
```

That script parses `DAL_M0001_FINAL_COMPARE` lines and computes weighted effect summaries plus leave-one-symbol and leave-one-timeframe stress summaries.
