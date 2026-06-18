# Decision Alpha Lab

A visual-first MQL5 research lab for validating market-structure hypotheses.

The active runtime is **MQL5-native**. M0001 is inspected directly on the MT5 chart. Excel/JSON report generation and external Python/UI bridge layers are not part of the active workflow.

## Active expert

```text
mql5/Experts/DecisionAlphaLab/M0001/M0001_LiveVisualLab.mq5
```

Apply to the local MQL5 folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\apply_mql_native_migration.ps1
```

Then compile:

```text
MQL5/Experts/DecisionAlphaLab/M0001/M0001_LiveVisualLab.mq5
```

## Current version

```text
M0001/M0002 research runtime: 1.73
```

## Runtime modes

### Fast research default

```text
InpRuntimeVisuals = false
InpDrawFinalVisuals = true
InpKeepVisualsOnDeinit = true
```

During the run the EA only appends newly closed candles. It does not recompute nodes/events/statistics or redraw chart objects on every candle. At shutdown it computes the full state once, prints final reports, draws the final chart, and keeps the drawings.

### Visual replay/debug mode

```text
InpRuntimeVisuals = true
```

The EA recomputes and redraws on every newly closed candle. It is still candle-gated, not tick-based, but it is slower because visual debugging is intentionally expensive.

## Inputs

```text
InpSymbol
InpTimeframe
InpBars
InpWarmupHistoricalBars

InpL
InpZoneRatio
InpExitGap
InpConsumeMode

InpShowNodes
InpShowZones
InpShowRevisits
InpShowEvents
InpShowRTV
InpShowState
InpShowExtremes
InpShowSummary
InpRuntimeVisuals
InpDrawFinalVisuals
InpKeepVisualsOnDeinit
```

## Input meaning

```text
InpSymbol                 empty = current chart symbol
InpTimeframe              PERIOD_CURRENT = current chart timeframe
InpBars                   0 = no cap
InpWarmupHistoricalBars   closed bars before the analysis period used to reconstruct old nodes

InpL                      structural node left/right confirmation window
InpZoneRatio              territory compression ratio
InpExitGap                outside-zone candles required to confirm touch
InpConsumeMode            HUNT mode or TOUCH mode
```

Visual toggles:

```text
InpShowNodes              node arrows + local node price text
InpShowZones              active/revisited/consumed territory zones
InpShowRevisits           true revisit labels only: REVISIT#1, REVISIT#2, ...
InpShowEvents             optional frozen event boxes
InpShowRTV                optional final-only RTV labels for rtv_ready events
InpShowState              pending/live/revisited/consumed/hunt state labels
InpShowExtremes           node-to-expansion-extreme audit lines
InpShowSummary            top-left chart summary
InpRuntimeVisuals         redraw during replay on each closed candle
InpDrawFinalVisuals       draw final audited chart state at shutdown
InpKeepVisualsOnDeinit    keep final chart objects after the test finishes
```

## M0001 algorithm lock

### 1. Structural node detection

A confirmed L-rule node is created only after right-side confirmation exists.

```text
HIGH node: high[i] >= left highs and high[i] >= right highs
LOW node:  low[i]  <= left lows  and low[i]  <= right lows

active_from_index = node_index + L
```

The marker is drawn on the pivot candle, but logic starts at `active_from_index`.

### 2. Territory construction

For a live LOW node:

```text
expansion_extreme = highest high in current tracking cycle
```

For a live HIGH node:

```text
expansion_extreme = lowest low in current tracking cycle
```

Territory is built around the original node price:

```text
distance = abs(expansion_extreme - node_price)
half_width = distance * (1 - zone_ratio)

territory_lower = node_price - half_width
territory_upper = node_price + half_width
```

### 3. Touch event

A touch event starts when a candle intersects the current live territory:

```text
bar.low <= territory_upper
bar.high >= territory_lower
```

At event entry, geometry freezes:

```text
event_lower
event_upper
event_extreme
```

The frozen event zone is used for exit-gap confirmation.

### 4. Touch confirmation

A touch is confirmed only when price stays fully outside the frozen event zone for:

```text
outside_count >= exit_gap
```

A candle intersects the frozen zone if its high/low overlaps that zone. Any overlap resets the outside counter.

### 5. HUNT

A node is hunted when its original node price breaks:

```text
LOW node:  bar.low  < node_price
HIGH node: bar.high > node_price
```

HUNT has priority before touch confirmation.

### 6. TOUCH mode

TOUCH mode is one-shot.

```text
first confirmed touch -> CONSUMED:TOUCH
hunt before confirmation -> CONSUMED:HUNT
```

There are no true revisits in TOUCH mode.

### 7. HUNT mode

HUNT mode supports true revisits.

```text
REV#0 = first visit
REV#1+ = true revisits
```

After a confirmed visit, the node stays alive:

```text
confirmed_touch_count += 1
next_revisit_id += 1
state = REVISITED LIVE
```

### 8. Revisited-live extreme reset

After each confirmed revisit in HUNT mode, the node keeps its identity and memory, but its expansion cycle resets:

```text
tracking_cycle_start = confirmation_index + 1
next expansion_extreme is measured from tracking_cycle_start
```

So a revisited live node is:

```text
same node_id
same node_price
same revisit memory
fresh post-visit expansion cycle
```

## RTV and logRTV

RTV uses scale-free candle volatility:

```text
candle_vol = abs(log(high / low))
RTV = average(inside_event_vol) / average(before_event_vol)
logRTV = log(RTV)
```

The baseline uses the same number of candles immediately before the event entry. For confirmed touches, the final `exit_gap` outside-zone confirmation candles are excluded from the inside RTV sample because they are confirmation candles, not inside-event volatility.

RTV is ready only after exit-gap closure and full baseline availability.

## Warmup and analysis_start

`InpWarmupHistoricalBars` seeds the stream with pre-test closed bars so old structural nodes are reconstructed before the real analysis period begins.

Final reports filter events by `analysis_start`, the first newly appended bar after warmup:

```text
event.entry_time >= analysis_start
```

Warmup can support old-node memory and before-window baselines, but warmup events are not counted in the final research sample.

## Final node/random reports

The compact logRTV node-vs-random report prints only at EA shutdown:

```text
DAL_M0001_FINAL_NODES
DAL_M0001_FINAL_RANDOM
```

The random line includes the `COMPARE` block with delta mean/median, win percentage, paired t-stat, Cohen d, and KS node-vs-random.

## Visual workflow

For a clean final chart:

```text
InpShowNodes = true
InpShowZones = true
InpShowRevisits = true
InpShowEvents = false
InpShowRTV = false
InpShowState = true
InpShowExtremes = false
InpShowSummary = true
InpDrawFinalVisuals = true
InpKeepVisualsOnDeinit = true
```

For deep state debugging:

```text
InpRuntimeVisuals = true
InpShowNodes = true
InpShowZones = true
InpShowRevisits = true
InpShowEvents = true
InpShowRTV = true
InpShowState = true
InpShowExtremes = true
InpShowSummary = true
```

## Important docs

```text
docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md
docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md
docs/mql_native/M0001_CANDLE_GATED_RUNTIME.md
docs/mql_native/MODULE_MAP.md
docs/mql_native/STRUCTURAL_NODE_MODULE_LOCK.md
```

## v1.60 Professional Validation Metrics

The M0001 MQL-native engine now includes a final-only professional validation layer: compact NODES/RANDOM reports, explicit effect-size metrics, paired validation, bootstrap confidence intervals, sign-flip permutation p-values, distribution-distance metrics, quantile/tail metrics, chronological split-stability metrics, optional parameter robustness, and an integrity audit. Histograms are optional (`InpPrintHistogram=false` by default) so Journal lines no longer truncate the core `COMPARE` metrics.

See `docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS.md`.

## M0001 stress validation

The MQL-native M0001 engine includes a final-only stress validation suite for hard matched nulls, placebo shifts, outlier removal, non-overlap events, cluster-robust diagnostics, block bootstrap, fixed-horizon stress, and negative controls. See:

- `docs/mql_native/M0001_STRESS_VALIDATION_SUITE.md`
- `docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT.md`

## M0002 reversal/continuation post-exit volatility hypothesis

The second active MQL-native hypothesis is separated into its own module and central Expert Advisor:

```text
MQL5/Experts/DecisionAlphaLab/M0002/M0002_ReversalContinuationExitVolatility.mq5
MQL5/Experts/DecisionAlphaLab/M0002/M0002_HuntRejectExitVolatility.mq5  # deprecated compatibility filename
```

M0002 reuses the M0001 structural-node detector, territory math, log-range utilities, and reporting metrics, but uses the exact M0001 completed-exit event sample. Its default measurement mode is `EVENT_RTV`, so the reported rawMean/rawMed are the same M0001-style event RTV values, split by reversal/continuation outcome. It does import M0001 hunt/touch/consume-filtered events as the H0002 research sample. After `exit_gap` fully-outside candles complete, it classifies the completed-exit candle by its side of the original node price:

```text
LOW / valley node: close above node => REVERSAL_AFTER_EXIT; close below node => CONTINUATION_AFTER_EXIT
HIGH / peak node: close below node => REVERSAL_AFTER_EXIT; close above node => CONTINUATION_AFTER_EXIT
```

It prints final-only branch reports once on deinit:

```text
DAL_M0002_FINAL_REVERSAL_AFTER_EXIT
DAL_M0002_FINAL_CONTINUATION_AFTER_EXIT
DAL_M0002_FINAL_REVERSAL_VS_CONTINUATION
```

The primary goal is to split the exact M0001 event-window RTV by the completed-exit node-side outcome and test whether the volatility expansion is concentrated in the reversal branch, concentrated in the continuation branch, or mixed across both branches. The optional post-outcome fixed-window mode is diagnostic only.

See `docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md`.


### M0002 v1.67 EVENT_RTV lock

M0002 reversal/continuation branch reports now hard-lock measurement to the native M0001 event RTV window. Branching is only a label assigned at completed neutral exit by close vs node_price; post-outcome fixed-window measurement is not exposed in the production H0002 EA.


## Logic repair v1.70

H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.

### M0001/M0002 v1.72 exit-gap clarification

M0001 exit confirmation is side-agnostic: the `exit_gap` candles must be fully outside the frozen territory, either on the rejection side or the break side. H0002 labels the exact M0001 completed events as reversal or continuation by close-vs-node at that completed exit candle; it does not force valid exits to be reversals.


### M0002 v1.73 branch model completion

H0002 now reports the branch model directly with:

```text
DAL_M0002_FINAL_BRANCH_MODEL
```

This line summarizes the observed reversal/continuation volatility model across count frequency, intensity, tail behavior, and post-event horizon memory. The working H0002 model is:

```text
reversal = higher-frequency, lower-intensity branch
continuation = lower-frequency, higher-intensity, higher-persistence, fatter-tail branch
```

See `docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md` for the full H0001/H0002 algorithm lock and hypothesis map.


## Current MQL-native hypothesis stack

- H0001: completed structural-node territory events produce higher RTV than matched random windows.
- H0002: continuation exits are lower-frequency but higher-intensity than reversal exits, with fatter tails and stronger post-event memory.
- H0003: continuation exits are tested as a volatility-memory state with inertia and time clustering using the same M0001/M0002 modules.

Key docs:

- `docs/mql_native/H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE.md`
- `docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md`
- `docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md`
