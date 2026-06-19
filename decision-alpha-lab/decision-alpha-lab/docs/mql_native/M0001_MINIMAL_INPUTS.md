# M0001 Minimal Inputs

## Decision

The M0001 expert Inputs panel has been reduced to a small operational set.

Old diagnostic, deprecated, report, styling, object-cap and internal stream-control
inputs have been removed from the Inputs panel.

## Current inputs

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

## Visual mapping

```text
InpShowNodes
-> node arrows
-> local node price text

InpShowZones
-> active live territory zones
-> consumed zone history

InpShowRevisits
-> true revisit labels only
-> REVISIT#1, REVISIT#2, ...
-> no TOUCH mode event text
-> no REV#0 first-visit text

InpShowState
-> pending labels
-> revisited-live labels
-> consumed labels
-> hunt markers

InpShowExtremes
-> node-to-expansion-extreme audit line

InpShowSummary
-> top-left chart summary
```

## Internal defaults

These are no longer user inputs:

```text
live stream = true
warmup historical bars = 0
start from next closed bar = true
closed bars only = true
compute on every tick = false
timer = 100 ms
draw only visible window = true
visible window padding = 80
purge trace lines = true
purge main-window indicators = true
node price text = true
active-from markers = false
event rectangles = false
RTV labels = false
visual caps = unlimited
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.44`.
