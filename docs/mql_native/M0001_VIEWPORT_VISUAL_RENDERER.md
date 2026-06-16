# M0001 Viewport Visual Renderer

## Problem

The M0001 engine can compute hundreds of nodes and audit states. Drawing every
node, every price label, every consumed marker, every extreme line, and every
hunt-zone rectangle on one MT5 chart can overload chart-object rendering.

This can look like nodes stop appearing after a point even though the detector is
still computing them.

## Fix

The renderer now defaults to viewport-based drawing:

```text
InpDrawOnlyVisibleWindow = true
InpVisibleWindowPaddingBars = 80
InpRedrawOnChartChange = true
```

The engine still computes all data. The chart only draws objects whose time range
intersects the currently visible chart window plus padding.

When the chart is scrolled or zoomed, `OnChartEvent(CHARTEVENT_CHART_CHANGE)`
redraws the objects for the new viewport.

## Important distinction

This is not a research/data limit.

```text
InpBars = 0
```

still means all tester/history bars.

Viewport rendering only limits the number of chart objects created at once, so
MT5 does not choke on thousands of objects.

## Summary

With diagnostics enabled, the summary shows:

```text
viewport=on <from> -> <to>
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.28`.
