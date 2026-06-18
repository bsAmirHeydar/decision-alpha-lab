# M0001 Node Arrow Tip Anchor Fix

## Problem

The node price was correct, but the red HIGH arrows appeared to sit on top of
candles because the visual glyph anchor was not the same as the visible arrow tip.

The user requirement is strict:

```text
The arrow tip must be exactly on the Python node price.
```

No visual price offset should be applied.

## Fix

MQL now draws the node arrow object at the exact Python `node_price` and changes
the arrow glyph anchor:

- HIGH node: down arrow, `ANCHOR_BOTTOM`
- LOW node: up arrow, `ANCHOR_TOP`

This makes the visible arrow tip sit on the node price.

## Input

```text
InpAnchorNodeArrowTip = true
```

## Important

The mathematical node price never changes.  
This is only a glyph-anchor fix in the MQL visual layer.
