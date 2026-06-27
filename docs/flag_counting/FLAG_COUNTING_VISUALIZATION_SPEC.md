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

The VNext implementation now detects ND / Hook phases as first-class text-only events, not only as gaps left after F rendering. For each active scale, the detector scans consecutive compressed node windows of 3 or 4 nodes and accepts a provisional ND when the window closes at least 50% toward its active extreme. This follows the documented rule that an ND does not need a 90% return; a minimum 50% extreme-close is enough for research visibility.

Important inputs:

- `InpScanND`: enables ND detection.
- `InpDetectAllND`: when true, scan all valid 3/4-node ND windows in each scale; when false, only unowned gaps are marked as ND.
- `InpMaxNDPerScale`: caps ND labels per scale for visual control.
- `InpNDMinNodes`: default 3.
- `InpNDMaxNodes`: default 4.
- `InpNDMinExtremeCloseRatio`: default 0.50.

ND is rendered as text only (`ND`) so it explains the partition without adding more body lines to the chart. Peak-side ND labels are placed above peaks and valley-side ND labels are placed below valleys using the same stacking system as F labels.
