# Phase 06 Hotfix003 — Dual-Symbol Full Visual Language

## Purpose

The previous visual layer could draw a divergence package on the attached chart or the hunter chart. That was not enough for the intended visual language. Intermarket divergence is a two-symbol condition, so the visual audit must exist on both symbol charts at the same time.

Hotfix003 changes the default visual behavior:

```text
SPXUSD chart receives the SPXUSD leg.
NDXUSD chart receives the NDXUSD leg.
Both charts receive synchronized visual evidence for the same signal id.
```

The chart is no longer treated as a single visual surface. The two input symbols are now treated as two synchronized audit surfaces.

## Current default

```text
InpDrawOnBothInputSymbolCharts = true
InpOpenMissingInputSymbolCharts = true
InpShowChartPanel = false
InpPrintSummaryOnNewClosedCandle = false
```

The expert can open missing charts for the two configured symbols. If the charts already exist, the expert uses them directly.

## Comments off

The chart `Comment()` panel is off by default. This removes the large text block from the chart.

Important distinction:

```text
Chart comments/panel = OFF by default.
Visual labels = ON by default.
Tooltips = ON through object tooltip metadata.
```

Visual labels are chart objects and are part of the drawing language. If the strategy architect later wants a purely line-based view, `InpDrawTextLabel` can be set to false.

## Symbol-local drawing principle

Every symbol chart receives its own price-scale-valid drawing package.

On the hunter symbol chart:

```text
origin = hunter reference extreme
destination = hunter current-cycle extreme
```

On the clean symbol chart:

```text
origin = clean reference extreme
destination = clean current-cycle extreme
```

This avoids drawing NDX prices on an SPX chart or SPX prices on an NDX chart.

## Confirmed tradeable signal visual structure

For a confirmed SELL divergence:

```text
hunter chart:
  reference high -> current high
clean chart:
  reference high -> current high that did not hunt
```

For a confirmed BUY divergence:

```text
hunter chart:
  reference low -> current low
clean chart:
  reference low -> current low that did not hunt
```

## Invalidated double-hunt state

For double-hunt invalidation, both symbol charts can still receive symbol-local visual packages using the newly preserved symbol-local reference and current-extreme fields:

```text
symbol A reference -> symbol A current extreme
symbol B reference -> symbol B current extreme
status = INVALIDATED_DOUBLE_HUNT
```

This is important because invalidated states are not ignored; they are part of the audit field.

## No strategy mutation

This patch changes visual representation only. It does not alter:

```text
cycle groups
reference logic
hunt logic
divergence logic
confirmation logic
invalidation logic
entry logic
risk logic
target logic
statistics
AI
```
