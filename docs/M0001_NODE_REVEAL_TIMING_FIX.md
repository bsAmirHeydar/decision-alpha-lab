# M0001 Node Reveal Timing Fix

## Problem

In a live-safe L-rule detector, a node located at candle `i` is not knowable at
candle `i`. It becomes knowable only after `L` right-side candles exist:

```text
active_from_index = node_index + L
```

If the visual marker is always drawn back on `node_index`, the chart can feel like
it is backpainting: the marker appears late but is placed on the older pivot candle.

## Fix

The Python visual contract now sends both times for every node:

```text
anchor_time = node/pivot time
end_time    = active_from/confirmation time
```

The MQL visual terminal can choose how to draw node markers:

```text
InpNodeMarkerTimeMode = 0  # draw on pivot candle, audit/backpaint view
InpNodeMarkerTimeMode = 1  # draw on active_from candle, live-reveal view
```

Default is `1`, which matches live decision semantics: the marker appears at the
time the node becomes knowable.

## Important

The node price remains the original Python node price in both modes.  
Only the marker time changes.
