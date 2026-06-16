# M0001 Revert Node Timing Mode and Fast Sync

## Revert

The `InpNodeMarkerTimeMode` experiment was removed.

Node markers are again drawn on the true pivot candle:

```text
anchor_time = node_time
price       = node_price
```

This keeps the visual geometry clear: the marker points to the actual structural
high/low.

## Live-safe rule

This is not a future leak because Python only receives candles up to the current
simulated closed bar from the MQL event bridge. A node at index `i` can only be
present in the visual contract after `L` right-side candles are available.

With `L=5`, the earliest possible confirmation is:

```text
current_closed_index >= i + 5
```

## Fast sync

The previous delay could come from bridge polling, not L-rule confirmation:

- Python watcher default refresh was 2000 ms
- MQL redraw timer was 2 seconds

For visual tester sync, defaults are now:

```text
InpBrainRefreshMs = 100
InpAutoReloadMilliseconds = 100
```

The MQL timer uses `EventSetMillisecondTimer()` when milliseconds are set, and
the Python watcher sleeps with a 50 ms lower bound.
