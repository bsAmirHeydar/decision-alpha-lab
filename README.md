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

## Minimal Inputs

The expert Inputs panel is intentionally small.

```text
InpSymbol
InpTimeframe
InpBars

InpL
InpZoneRatio
InpExitGap
InpConsumeMode

InpShowNodes
InpShowZones
InpShowRevisits
InpShowState
InpShowExtremes
InpShowSummary
```

Everything else is now an internal default, not an input.

## Input meaning

```text
InpSymbol       empty = current chart symbol
InpTimeframe    PERIOD_CURRENT = current chart timeframe
InpBars         0 = no cap

InpL            structural node left/right confirmation window
InpZoneRatio    territory compression ratio
InpExitGap      candles outside frozen event zone required to confirm touch
InpConsumeMode  HUNT mode or TOUCH mode
```

Visual toggles:

```text
InpShowNodes      node arrows + local node price text
InpShowZones      active/consumed territory zones
InpShowRevisits   true revisit labels only: REVISIT#1, REVISIT#2, ...
InpShowState      pending/live/consumed/hunt state labels
InpShowExtremes   node-to-expansion-extreme audit lines
InpShowSummary    top-left run summary
```

## M0001 algorithm

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

The frozen event zone is used until the event closes.

### 4. Touch confirmation

A touch is not confirmed immediately. It becomes confirmed only when price stays outside the frozen event zone for:

```text
outside_count >= exit_gap
```

Before confirmation, HUNT has priority.

### 5. HUNT

A node is hunted when its original node price breaks:

```text
LOW node:  bar.low  < node_price
HIGH node: bar.high > node_price
```

If this happens during a pending touch, the event closes as HUNT and the node is consumed by HUNT.

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

The node is still the same node, but it now has memory that its territory was tested.

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

## Clean visual workflow

For a clean chart:

```text
InpShowNodes = true
InpShowZones = true
InpShowRevisits = true
InpShowState = false
InpShowExtremes = false
InpShowSummary = true
```

For deep state debugging:

```text
InpShowNodes = true
InpShowZones = true
InpShowRevisits = true
InpShowState = true
InpShowExtremes = true
InpShowSummary = true
```

## Version

Current expert version: `1.44`.


## Live zone resync

The active zone box now follows the current cycle extreme while the node is
alive. Frozen pending-touch geometry is used only for exit-gap confirmation, not
for the live zone rectangle.

```text
alive node -> territory follows current tracking_extreme
pending event -> frozen internally for confirmation
confirmed revisit in HUNT mode -> tracking cycle resets
live box starts from tracking_cycle_start_time
```

The rectangle renderer also upserts coordinates so an existing zone object is
moved instead of leaving stale coordinates behind.


## Node-origin zones and revisit colors

Live zone rectangles are now always drawn from the structural node candle:

```text
rectangle_start_time = node_time
```

This does not undo revisit extreme reset. After confirmed revisits, the price
geometry still uses the post-visit reset cycle, but the rectangle's time origin
stays on the original node for visual clarity.

Revisit text colors:

```text
LOW / valley revisit  -> blue
HIGH / peak revisit   -> red
```


## Revisited zone colors

After at least one confirmed revisit, live hunt-zone rectangles change color:

- HIGH / peak revisited zone -> purple
- LOW / valley revisited zone -> blue

Consumed historical zones still use the inactive gray style.


## RTV log high/low

RTV now uses scale-free candle volatility:

```text
candle_vol = abs(log(high / low))
RTV = average(inside_event_vol) / average(before_event_vol)
```

The baseline uses the same number of candles immediately before the event entry.
For confirmed touches, the final `exit_gap` outside-zone candles are excluded
from the inside RTV sample because they are confirmation candles, not inside-event
volatility.

Enable labels with:

```text
InpShowRTV = true
```


## RTV summary comment and text file

M0001 now continuously shows the mean and median of all final ready RTV values in
the chart comment.

It also writes ready RTV rows to:

```text
DAL_M0001_RTV_<symbol>_<timeframe>.txt
```

The text file contains one row per `rtv_ready=true` event, including sample length,
baseline start, inside end, mean_before, mean_inside and final RTV.


## RTV waits for exit-gap closure

RTV is now marked ready only after the frozen event zone has been exited for
`exit_gap` consecutive candles by high/low. Any candle that intersects the zone
resets the outside counter.

HUNT-before-confirmation events remain visible for audit, but they are not
included in final RTV mean/median because the exit-gap closure was never completed.


## RTV final-only labels

RTV labels are now drawn only after the event is fully closed and `rtv_ready=true`.
Unfinished events no longer show `RTV n/a` on the chart. The chart, mean/median,
and text export now all use the same final-only RTV rule.


## RTV distribution report

M0001 includes a separate RTV distribution module:

```text
mql5/Include/DecisionAlphaLab/M0001/DAL_M0001RtvDistribution.mqh
```

It prints a copyable Journal report between:

```text
DAL_M0001_RTV_DISTRIBUTION_REPORT_BEGIN
DAL_M0001_RTV_DISTRIBUTION_REPORT_END
```

The report includes mean, median, percentiles, variance, skewness, excess
kurtosis, Jarque-Bera, KS distance, Anderson-Darling, 2σ/3σ tail ratios against
normal expectations, robust tail ratios, and a TSV histogram.


## LogRTV random null comparison

M0001 now compares final node RTV against a matched random baseline using:

```text
logRTV = log(mean_inside / mean_before)
```

The compact Journal line is:

```text
DAL_M0001_LOGRTV_NULL *** NODES ... *** RANDOM ... *** COMPARE ...
```

The old verbose multi-line distribution report and the per-bar status print are
disabled by default to reduce Journal noise and runtime overhead.


## Final node/random reports

The compact logRTV node-vs-random report now prints only at EA shutdown:

```text
DAL_M0001_FINAL_NODES
DAL_M0001_FINAL_RANDOM
```

This removes runtime Journal noise. The final random line also includes the
`COMPARE` block with delta mean/median, win percentage, paired t-stat, Cohen d,
and KS node-vs-random.


## Final-only research report and warmup seed

M0001 now computes professional logRTV node-vs-random statistics only once at shutdown. Runtime distribution-stat calculations and file-report logic were removed from the live loop.

A new input, `InpWarmupHistoricalBars`, seeds the stream with pre-test closed bars so old structural nodes are reconstructed before the test period begins. Final reports filter events by `analysis_start`, the first newly appended bar after warmup, so old nodes can be touched during the test without including pre-test events in the research sample.

Unused legacy MQL report/validation files were removed to keep the runtime tree cleaner.


## Fast final-only runtime

M0001 defaults to `InpRuntimeVisuals=false`, which keeps the live stream in
memory during the run and delays all expensive node/event/statistical work until
`OnDeinit`. This prevents full recomputation and chart redraw on every closed bar.

The final Journal report still prints one NODES line and one RANDOM/COMPARE line.
`.venv/` and `venv/` are ignored because the MQL-native branch does not require a
local Python virtual environment.
