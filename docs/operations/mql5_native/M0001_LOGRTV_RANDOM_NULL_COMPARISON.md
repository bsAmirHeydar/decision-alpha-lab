# M0001 LogRTV Random Null Comparison

## Purpose

Raw RTV is useful for interpretation, but it is naturally bounded below and
unbounded above. Statistical comparison is therefore done on:

```text
logRTV = log(mean_inside / mean_before)
```

This makes a 2x expansion and a 0.5x contraction symmetric:

```text
RTV 2.0 -> logRTV +0.693
RTV 0.5 -> logRTV -0.693
```

## Node sample

The node sample uses final M0001 events only:

```text
event.closed == true
event.rtv_ready == true
event.rtv > 0
```

## Random null sample

For every ready node event, a matched random reference window is generated:

```text
same rtv_sample_length
random entry point in the same market series
same before-window length immediately before the random entry
same log high/low candle volatility formula
```

This creates a parallel random baseline using the same measurement structure.

## Journal output

All extra per-bar prints are disabled by default. The EA prints one compact line
only when the node-vs-random logRTV result changes:

```text
DAL_M0001_LOGRTV_NULL *** NODES ... *** RANDOM ... *** COMPARE ...
```

The line contains:

```text
rawMean/rawMed/rawP90/rawP95
logMean/logMed/logGt0Pct
skew/excessKurt/JB/KS-to-normal
tail2/tail3 ratios vs normal
compact raw histogram counts
node-vs-random delta mean/median
paired win percentage
paired t-stat
Cohen d
KS node-vs-random
```

## Performance

The huge multi-line distribution report and the standard per-bar status print are
disabled. The compact result is throttled by signature, so it only prints when
ready RTV statistics actually change.

## Version

`M0001_LiveVisualLab.mq5` version: `1.54`.
