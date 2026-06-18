# M0001 / H0001 Logic Repair Audit

Date: 2026-06-18

This document records the logic audit performed before repairing M0002.

## H0001 active hypothesis

Structural node territories condition future volatility expansion more than matched random windows.

## Locked structural-node logic

- Bars are chronological: oldest to newest.
- A HIGH node at index `i` requires:
  - `high[i] >= high[i-L..i-1]`
  - `high[i] >= high[i+1..i+L]`
- A LOW node at index `i` requires:
  - `low[i] <= low[i-L..i-1]`
  - `low[i] <= low[i+1..i+L]`
- Node becomes knowable at:

```text
active_from_index = node_index + L
```

## Locked territory logic

```text
distance = abs(tracking_extreme - node_price)
half_width = distance * (1 - zone_ratio)
territory_lower = node_price - half_width
territory_upper = node_price + half_width
```

For LOW nodes, the tracking extreme is the highest high after the active-from point. For HIGH nodes, it is the lowest low after the active-from point.

## Locked M0001 event/RTV logic

- Event starts when a candle intersects the live territory.
- The event territory freezes at event entry.
- Exit confirmation requires `exit_gap` consecutive candles fully outside the frozen event zone.
- A candle whose high/low intersects the frozen event zone resets the outside counter.
- RTV is calculated only after touch/exit confirmation.
- Final `exit_gap` outside-zone confirmation candles are excluded from the inside sample.
- Baseline window is equal length and immediately before event entry.

```text
inside_length = event_length - exit_gap
mean_inside = mean(abs(log(high / low))) over entry..entry+inside_length-1
mean_before = equal-length mean before entry
RTV = mean_inside / mean_before
logRTV = log(RTV)
```

## Locked anti-lookahead rules

- Node is used only after `active_from_index`.
- Warmup bars are used to seed old structural memory only.
- Final reports count only events with `entry_time >= analysis_start`.
- Baseline is always before event entry.
- Random windows use the same sample length and a valid before-window.

## Result of audit

No H0001 formula change was required in this repair. M0001 remains the source of truth for structural node detection, territory geometry, completed-exit event semantics, event RTV, logRTV, random baseline, stress validation, and final visual state.

The actual bug was in H0002: it was measuring post-outcome fixed-window volatility by default rather than splitting the original M0001 event-window RTV by reversal/continuation. H0002 is now repaired so its default metric is `EVENT_RTV`.
