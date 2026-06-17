# M0001 Professional Validation Metrics — v1.60

This document locks the professional validation layer added to the M0001 MQL-native research engine. The node, territory, touch, HUNT, revisit, RTV, logRTV, warmup, and candle-gated runtime semantics are unchanged.

## Final-only validation design

The EA remains candle-gated during runtime:

```text
intra-candle tick -> return
new candle open -> append previous closed candle once
OnDeinit -> compute full node/event/audit state once
OnDeinit -> print final validation reports once
OnDeinit -> draw final visual state once if enabled
```

The professional statistics are intentionally final-only. They are not recalculated on every candle.

## Compact report bug fix

Earlier reports embedded `histRaw` into the main NODES/RANDOM lines. Long histograms could be truncated by the MetaTrader Journal, hiding the important `COMPARE` section.

v1.60 fixes this by default:

```text
InpPrintHistogram = false
```

The main final lines are compact and the histogram is printed only as separate optional `DAL_M0001_FINAL_HIST_*` lines.

## Random baseline K

Each node event can now be compared against multiple matched random windows:

```text
InpRandomSamplesPerEvent = 20
```

For each valid node event, the engine builds a deterministic random baseline with the same RTV sample length and a valid pre-entry before-window. The random logRTV for that event is the mean of the valid K matched random logRTVs. This reduces one-random-draw noise while preserving the same null hypothesis idea.

## Core outputs

### NODES / RANDOM

Each distribution reports:

```text
n
rawMean, rawMed, rawP75, rawP90, rawP95
rawCVaR90, rawCVaR95
logMean, logMed, logGt0Pct, logIQR
skew, excess kurtosis, Jarque-Bera, KS-normal
tail2xN, tail3xN
```

### COMPARE

The node-vs-random report includes effect size and pairwise validation:

```text
dLogMean
geoRatio = exp(dLogMean)
dLogMed
medianRatio = exp(dLogMed)
dGt0Pct
pairedWinPct
pairedMeanDelta
pairedMedianDelta
pairedT
tPapprox
cohenD
signPapprox
cliffDelta
KS
CvM
W1log
```

### QUANT_TAIL

Quantile and tail opportunity metrics:

```text
dQ50, dQ75, dQ90, dQ95
dCVaR90, dCVaR95
rightTailOdds
```

### ROBUST

Robustness and stability metrics:

```text
bootstrap dMean CI95
bootstrap winPct CI95
sign-flip permutation p-value
chronological split positive percentage
min split dLog
mean split dLog
split dLog standard deviation
min split winPct
stabilityScore
```


### SESSION_REGIME

Session and simple regime robustness are printed as:

```text
DAL_M0001_FINAL_SESSION_REGIME
```

The session split uses broker-hour buckets:

```text
Asia: 00:00-07:59
London: 08:00-15:59
New York / late session: 16:00-23:59
```

The regime split uses matched-random logRTV terciles:

```text
low random-log regime
middle random-log regime
high random-log regime
```

For each bucket the report prints `N`, mean paired `dLog`, and paired win percentage.

### AUDIT

Integrity checks are printed in a separate final line:

```text
closed events
events after analysis_start
warmup-excluded events
rtv-ready events
paired events
baselineOkPct
touchConfirmedPct
pairedPctOfReady
randomK
histogram on/off
lookaheadGuard
baselineGuard
exitGapGuard
```

## Optional parameter robustness grid

Set:

```text
InpRunParameterRobustness = true
```

The engine then runs an optional final-only parameter grid around the active settings:

```text
L: current L ± 2
zoneRatio: current zone ± 0.05
exitGap: current gap ± 1
```

It prints:

```text
DAL_M0001_FINAL_PARAM_ROBUST
```

with:

```text
combos
valid
minN
robustParamPct
positiveMedianPct
winOver50Pct
meanDLog
medianDLog
minDLog
maxDLog
meanWinPct
```

The grid is optional because it recomputes the full M0001 state for many nearby parameter settings.

## Semantics preserved

v1.60 does not redefine:

```text
L-rule node detection
active_from = node_index + L
territory formula
touch event geometry
frozen event zone
strict exit_gap confirmation
HUNT priority
TOUCH mode
HUNT mode
REV#0 / REV#1+
revisited-live extreme reset
RTV = mean_inside / mean_before
logRTV
analysis_start filtering
warmup node memory
final restored visuals
```
