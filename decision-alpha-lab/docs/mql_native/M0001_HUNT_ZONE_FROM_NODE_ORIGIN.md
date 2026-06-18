# M0001 Hunt Zone Origin From Node

## Change

Live hunt/territory rectangles now start from the original structural node time,
not from `active_from_time`.

Before:

```text
rectangle_start = active_from_time
```

Now:

```text
rectangle_start = node_time
```

The rectangle still extends to:

```text
current live-stream bar
```

or, for invalidated nodes when enabled:

```text
invalidated_time
```

## Why

The visual audit should show the full territory relationship from the node origin.
The node itself remains the structural anchor, while `active_from_time` remains the
live-safe confirmation point used by the logic.

## Important

This is a visual-origin change only.

The detector still confirms nodes using the L-rule:

```text
active_from_index = node_index + L
```

The M0001 logic still uses confirmed nodes only. The rectangle simply begins at
the node candle to make the territory's structural origin visually clear.

## Version

`M0001_LiveVisualLab.mq5` version: `1.21`.
