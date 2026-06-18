# M0001 Latest Visual Caps

## Problem

Positive visual caps such as:

```text
InpMaxNodesToDraw = 2
```

were limiting the renderer to the first/oldest two nodes.

That made it look like nodes stopped appearing later in the test, even though the
engine was still computing them.

## Fix

Positive visual caps now draw the latest N items:

```text
InpMaxNodesToDraw = 2       -> latest 2 nodes
InpMaxEventsToDraw = 2      -> latest 2 events
InpMaxAuditStatesToDraw = 2 -> latest 2 audit states
```

## Data cap vs visual cap

`InpBars` is a data limit, not a drawing limit:

```text
InpBars = 0  -> all tester/history bars
InpBars = 2  -> only keep 2 bars of data
```

For normal backtests keep:

```text
InpBars = 0
```

and control chart clutter with the visual caps:

```text
InpMaxNodesToDraw = 50
InpMaxAuditStatesToDraw = 50
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.26`.
