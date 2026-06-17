# M0001 Final Visuals and Logic Lock

Version: 1.59

This document locks the current M0001 research semantics and runtime contract.
It exists so future optimization work does not accidentally change the algorithm.

## Runtime contract

M0001 is candle-based, not tick-based.

```text
intra-candle tick -> immediate return
new candle opens -> append the previous closed candle once
shutdown / deinit -> compute full node/event/audit/statistical state once
```

The optimized default is:

```text
InpRuntimeVisuals = false
InpDrawFinalVisuals = true
InpKeepVisualsOnDeinit = true
```

That means:

- no full node/event recomputation on every closed candle,
- no chart object deletion/redraw loop during the test,
- final node/random logRTV reports are printed once at shutdown,
- final chart objects are restored and kept after the run finishes.

For visual debugging during a replay, set:

```text
InpRuntimeVisuals = true
```

This intentionally costs more because the chart state is recomputed and redrawn on each newly closed candle.

## Structural node definition

A confirmed L-rule node at index `i` requires both left and right confirmation windows.

```text
HIGH node: high[i] >= every high in i-L ... i-1
        and high[i] >= every high in i+1 ... i+L

LOW node:  low[i] <= every low in i-L ... i-1
        and low[i] <= every low in i+1 ... i+L

active_from_index = node_index + L
```

The node marker is drawn on the pivot candle. Trading/research logic starts only from `active_from_index`.

## Territory formula

For LOW nodes, the expansion extreme is the highest high in the current tracking cycle.
For HIGH nodes, the expansion extreme is the lowest low in the current tracking cycle.

```text
distance = abs(expansion_extreme - node_price)
half_width = distance * (1 - zone_ratio)
territory_lower = node_price - half_width
territory_upper = node_price + half_width
```

The territory is always centered on the original structural node price.

## Event lifecycle

1. Start scanning from `active_from_index`.
2. Update the node-level tracking extreme while the node is alive.
3. Build the live territory from the current tracking extreme.
4. Start an event when high/low intersects the live territory.
5. Freeze event geometry at entry:
   - `event_lower`
   - `event_upper`
   - `event_extreme`
6. Confirm the touch only after `exit_gap` consecutive candles whose high/low do not intersect the frozen event zone.
7. Any candle intersecting the frozen zone resets the outside counter.

## HUNT priority

Before touch confirmation, HUNT has priority.

```text
LOW node hunted:  bar.low < node_price
HIGH node hunted: bar.high > node_price
```

If HUNT happens during a pending event, the node is consumed by HUNT and that event is not RTV-ready.

## TOUCH mode

TOUCH mode is one-shot.

```text
first confirmed touch -> CONSUMED:TOUCH
hunt before confirmation -> CONSUMED:HUNT
```

TOUCH mode does not expose true revisit labels.

## HUNT mode and revisit memory

HUNT mode allows repeated confirmed touches before the original node price breaks.

```text
REV#0 = first confirmed visit
REV#1+ = true revisits
```

After each confirmed visit:

```text
confirmed_touch_count += 1
next_revisit_id += 1
state = REVISITED LIVE
```

The node keeps the same identity and original node price.

## Revisited-live extreme reset

After a confirmed revisit in HUNT mode, the next tracking cycle starts after the confirmation candle.

```text
tracking_cycle_start_index = confirmation_index + 1
tracking_extreme = first bar of the new cycle
```

This resets the price geometry for the next territory, but it does not change the node identity.

## Visual rules

Final visual objects are generated from the same computed arrays used by the final report:

```text
bars -> nodes -> events -> audit_states -> final reports + final visuals
```

So chart drawings and final metrics cannot drift from each other.

Default visual behavior:

- node arrows and local node price labels are restored,
- live/consumed hunt zones are restored,
- true revisit labels are restored,
- state labels and consumed labels are restored,
- optional event boxes are available through `InpShowEvents`,
- optional final RTV labels are available through `InpShowRTV`,
- objects are kept after `OnDeinit` when `InpKeepVisualsOnDeinit=true`.

Live zone rectangles visually start from the structural node candle:

```text
rectangle_start_time = node_time
```

After a confirmed revisit, price geometry uses the reset extreme cycle, but the visible rectangle keeps the structural node as its time origin.

## RTV and logRTV

Per-candle volatility is scale-free:

```text
candle_vol = abs(log(high / low))
```

Final RTV uses the same number of inside and before candles:

```text
RTV = mean_inside_log_range / mean_before_log_range
logRTV = log(RTV)
```

The final `exit_gap` outside-zone confirmation candles are excluded from the inside sample.

An event is RTV-ready only if:

```text
touch_confirmed == true
rtv_sample_length > 0
full before-window exists
mean_before > 0
```

## Warmup and analysis period

`InpWarmupHistoricalBars` loads older closed bars at initialization so structural nodes that existed before the test window are reconstructed.

The final research sample is filtered by `analysis_start`, the first newly appended bar after warmup:

```text
event.entry_time >= analysis_start
```

Warmup can support old-node memory and before-window baselines, but warmup events are not counted in the final research sample.

## Random baseline

The random baseline uses matched windows:

- same sample length as the ready node event,
- same log-range volatility formula,
- before-window immediately before the random entry,
- random entry constrained to the same analysis period.

The final report prints:

```text
DAL_M0001_FINAL_NODES
DAL_M0001_FINAL_RANDOM
```

The random line includes `COMPARE` values for paired node-vs-random analysis.
