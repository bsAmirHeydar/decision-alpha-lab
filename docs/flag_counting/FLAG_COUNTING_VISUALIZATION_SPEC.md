# Flag Counting Visualization Specification

This document defines how Flag Counting structures must be rendered on chart. It is a display contract, separate from the detector logic.

## 1. Purpose

The chart must be readable even when many scales and sequences are active at the same time. Rendering must not turn the chart into a pile of overlapping text and crossing labels.

The renderer must therefore use:

- scale-aware priority,
- F-level-aware priority,
- stacked labels,
- body-only path drawing,
- direction/status colors,
- larger lines and labels for larger scales.

## 2. Body-only drawing

Each F body is drawn as:

1. `Origin -> Leg1`: straight trend line.
2. `Leg1 -> Waist -> Leg2`: one smooth curve whose belly is tangent to the Waist node.

The renderer must not draw post-Leg2 continuation lines to internal `1`, internal `2`, confirmation, or invalidation. Internal `1/2` are rendered as numbers only.

## 3. Display priority

When multiple labels collide, the dominant label must be closest to the price structure.

Priority order:

1. Larger `scaleL` first.
2. Higher F-level first: `F3 > F2 > F1`.
3. Stronger status first: `terminal > confirmed > live`.
4. Larger body size first.

## 4. Label stacking rule

For bullish F bodies, `Leg2` is a peak. The `F1/F2/F3` label is placed above the peak.

- Slot 0 is closest to price.
- Higher-priority labels receive slot 0.
- Lower-priority labels are stacked above slot 0.

For bearish F bodies, `Leg2` is a valley. The `F1/F2/F3` label is placed below the valley.

- Slot 0 is closest to price.
- Higher-priority labels receive slot 0.
- Lower-priority labels are stacked below slot 0.

This matches the visual rule:

- In valleys, the highest text in the stack is the strongest / largest-scale / highest-F label.
- In peaks, the lowest text in the stack is the strongest / largest-scale / highest-F label.

## 5. Scale-aware sizing

Larger scales must be more visible.

Recommended defaults:

- `L < 5`: width 1, base font.
- `L >= 5`: width 2, font +1.
- `L >= 8`: width 3, font +2.
- `L >= 13`: width 4, font +3.
- `L >= 21`: width 5, font +4.

## 6. Color contract

The renderer uses four main colors:

- bullish live,
- bullish confirmed,
- bearish live,
- bearish confirmed.

F3 terminal movement may optionally have a special color for bullish and bearish terminal states.

## 7. Layering

Bodies must be drawn first. Labels must be drawn second. This keeps labels readable on top of body curves.

## 8. Acceptance criteria

A visualization is acceptable when:

- the chart shows F bodies without post-Leg2 path clutter,
- labels are not piled on the same point,
- larger scale labels stay closer to the structure,
- higher F-level labels stay closer to the structure when scale is equal,
- bullish and bearish structures are visually distinct,
- live and confirmed states are visually distinct,
- the user can identify the scale hierarchy without opening logs.

## Clean-All Visualization Update

The renderer should not hide accepted sequences by default. Instead, it makes every visible sequence easier to read:

- All F body lines use the same thin width by default (`InpFixedLineWidth = 1`).
- Larger scales no longer become visually heavier by line width; scale remains available through labels, logs, and sequence identity.
- Each sequence receives a subtle shade variation inside its own direction/status color family (`InpUseSequenceColorShades = true`).
- Bullish, bearish, live, confirmed, F3 terminal, and ND color families remain distinct, but individual sequence shades help separate overlapping paths.
- ND / Hook phases are text-only labels (`ND`) and do not draw additional body lines. This keeps the chart informative without adding line noise.
- The visual objective is to show all accepted/provisional structures while preventing scale thickness and repeated labels from overwhelming the price chart.

Relevant inputs:

- `InpScanND`
- `InpDrawND`
- `InpMaxNDPerScale`
- `InpUseSequenceColorShades`
- `InpFixedLineWidth`
- `InpNDColor`

