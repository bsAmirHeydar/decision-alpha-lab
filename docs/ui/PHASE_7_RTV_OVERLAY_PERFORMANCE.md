# Phase 7 RTV Overlay Performance Fix

## Problem

After the candle time fix, the chart correctly loaded thousands of candles, but the visual replay became slow and the RTV values were not obvious on the chart.

The reason was that the frontend tried to render thousands of HTML overlay objects at once:

- actual territories
- event windows
- RTV labels
- node markers
- hunt markers
- random baseline layers

Rendering all of those across 5000 candles creates many DOM nodes and makes panning/zooming laggy.

## Fix

### Viewport-based overlay rendering

The chart now only projects objects that intersect the currently visible logical range.

### Level-of-detail limits

When zoomed far out:

- dense territory/event rectangles are suppressed
- top RTV labels remain visible
- hunt markers and reference markers remain visible
- selected/hovered objects are always kept

When zoomed in:

- event windows and territories render normally
- more RTV labels become visible

### Faster candle updates

Replay no longer calls `series.setData()` on every single step. It uses:

- `setData()` only for dataset changes, rewinds, or large jumps
- `series.update()` for forward step-by-step replay

### Clearer RTV labels

RTV badges are placed near the event midpoint instead of the event entry candle.

Color logic:

- strong RTV: amber
- weak RTV: red/pink
- neutral RTV: cyan
- random RTV: amber-brown theme

## Result

The chart should now feel much smoother and the RTV values should be inspectable directly on the chart while still letting the user toggle each layer.
