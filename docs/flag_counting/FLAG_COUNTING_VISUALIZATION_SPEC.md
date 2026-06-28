<!-- CURRENT CANON NOTICE
This file is retained as historical/context documentation. For current Phoenix implementation decisions, use:

docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md

If this file conflicts with the current canon, the current canon wins.
-->

# Flag Counting Visualization Specification

This document defines the clean-all chart visualization for `FlagCountingVNext`.

## Core display contract

The renderer must allow all accepted F and ND sequences to remain visible, but it must avoid turning the chart into unreadable noise.

The default visual contract is:

- all body lines use the same thin width;
- different sequences use shade variations inside the same direction/status color family;
- peak labels are placed above peaks;
- valley labels are placed below valleys;
- labels are stacked deterministically when several F/ND labels belong to the same visual cluster;
- the closest label to price is the dominant one: larger scale first, then higher F level, then stronger status;
- ND/Hook phases are text-only labels and do not draw additional body lines;
- F bodies are drawn as `Origin -> Leg1` straight line plus a smooth arc-like curve from `Leg1 -> Waist -> Leg2`.

## Label stacking

Labels must not be placed with arbitrary offsets. They are assigned stack slots by priority.

Priority order:

1. larger `scaleL`
2. higher F level: `F3 > F2 > F1 > ND`
3. stronger status: `terminal > confirmed > live`
4. larger body size
5. older/stable event id

For peak-side anchors, labels are stacked upward above the peak. For valley-side anchors, labels are stacked downward below the valley.

## ND labels

ND labels use the same stack system as F labels. ND must remain text-only by default to avoid adding extra line noise.

## Curves

The body curve must not look like a broken zig-zag. The renderer uses dense Bezier sampling so the curve looks like a continuous arc. The curve must touch the main correction/waist region visually and terminate cleanly at Leg2.

## Line widths

All sequence body lines should be thin by default. Scale must not thicken lines in clean-all mode.

## ND / Hook Detection Contract

The VNext implementation now detects ND / Hook phases as first-class text-only events, not only as gaps left after F rendering. For each active scale, the detector scans consecutive compressed node windows of 3 or 4 nodes and accepts a provisional ND when the final high/low node reaches at least 50% toward the active extreme of that node window. This follows the documented rule that an ND does not need a 90% return; a minimum 50% high/low extreme ratio is enough for research visibility.

Important inputs:

- `InpScanND`: enables ND detection.
- `InpDetectAllND`: when true, scan all valid 3/4-node ND windows in each scale; when false, only unowned gaps are marked as ND.
- `InpMaxNDPerScale`: caps ND labels per scale for visual control.
- `InpNDMinNodes`: default 3.
- `InpNDMaxNodes`: default 4.
- `InpNDMinExtremeRatio`: default 0.50.

ND is rendered as text only (`ND`) so it explains the partition without adding more body lines to the chart. Peak-side ND labels are placed above peaks and valley-side ND labels are placed below valleys using the same stacking system as F labels.

### ND high/low-only contract

ND / Hook detection is close-agnostic. It does not care whether a candle closed beyond a level or not. The whole flag-counting grammar currently treats the market through swing highs and swing lows only. ND windows are therefore evaluated from compressed high/low nodes:

- valid ND windows use 3 or 4 alternating high/low nodes;
- the final ND node must reach the configured side of the window by at least `InpNDMinExtremeRatio`;
- `InpNDMinExtremeRatio = 0.50` means the last swing node is at least in the relevant half of the high-low range of that ND window;
- candle open, candle close, candle body, and candle color are not part of the ND definition.



## Origin identity and live-root display contract

The renderer must show coherent live roots by default. A root F1 body does not need to be hidden until internal `1/2` and confirmation; otherwise the chart becomes artificially empty and the research view loses the developing structures. Strict root filters remain optional audit inputs, but their defaults are off.

Orphan control comes from origin identity: if a candidate touches or crosses its own Origin / start of leg, that candidate is invalid and must not be drawn or extended. If it is a child, only the child dies; the parent remains alive unless its own invalidation is hit.

Each rendered F body keeps a traceable identity through `F#/L#/Q#` labels and an `O` origin label, so the chart shows which flag/scale/sequence owns each body and where its first leg starts. ND remains high/low-node based and close-agnostic.
