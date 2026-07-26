# M0001 MQL-Native Specification

## L-rule node

A node at index `i` is confirmed only when `L` right-side candles exist.

For `L = 5`:

```text
left  side: i-5 ... i-1
pivot:      i
right side: i+1 ... i+5
```

The node is available in a live-safe stream when:

```text
latest_closed_index >= i + L
```

The visual marker is drawn on the pivot candle, not on the confirmation candle.

## RTV event

For each confirmed node:

1. Start scanning from `active_from_index = node_index + L`.
2. Expand the opposite extreme.
3. Build a territory around the node price.
4. Start an event when a candle intersects the territory.
5. Close the event after `exit_gap` outside candles.
6. Compute:

```text
RTV = mean_inside_log_range / mean_before_log_range
```

## Runtime Guarantee

The native Expert reads candles directly from MT5. No external bridge, file watcher, or asynchronous process is involved.
