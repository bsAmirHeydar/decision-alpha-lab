---
type: architecture
product: gartal terminal
status: active
language: en
tags:
  - chart-rendering
  - mt5-objects
  - timeline
---

# 08 — Chart Rendering Object Model

## Goal

Render news events directly on the chart without visual noise, object collisions, or heavy redraw cost.

The chart has two rendering surfaces:

1. **event vertical lines** at broker event time;
2. **bottom future timeline strip** that shows the rest of the day's upcoming events ahead of price.

## Object Prefixes

Every object must use a deterministic prefix.

| Surface | Prefix |
|---|---|
| Dashboard | `GT_DASH_` |
| Vertical event lines | `GT_LINE_` |
| Event labels | `GT_LABEL_` |
| Bottom timeline | `GT_TL_` |
| Diagnostics | `GT_DIAG_` |

No renderer may delete objects outside its own prefix.

## Vertical Line Model

For each visible event within render range:

```text
GT_LINE_{event.id}
GT_LABEL_{event.id}
```

Line style:

| Impact | Line Style |
|---|---|
| High | strong, visible, red impact color |
| Medium | medium thickness / orange impact color |
| Low | thin / yellow impact color |
| Holiday | dotted / gray |
| Tentative | dashed |
| Breaking | high impact + pulse/strong label |

## Label Placement

Label text:

```text
15:30 USD HIGH — NFP
```

Compact label:

```text
USD NFP
```

Label collision policy:

- group nearby events;
- offset row labels vertically;
- cap maximum labels per cluster;
- show full detail in dashboard.

## Bottom Timeline Strip

Purpose: show upcoming news before price reaches those chart times.

The strip is drawn in chart pixel space near the bottom.

Objects:

```text
GT_TL_BG
GT_TL_AXIS
GT_TL_EVENT_{event.id}
GT_TL_LABEL_{event.id}
```

Mapping:

```text
time_range = day_start_broker -> day_end_broker
x_position = normalized event broker time within visible chart width or terminal panel width
```

V1 can use chart coordinate helpers. If exact pixel mapping is unstable, use a fixed panel-style strip anchored to corner.

## Future Projection Rule

Events after the latest visible candle should still be displayed.

For MT5 vertical lines, future datetime objects can render beyond current price if the chart has shift/future space. The bottom strip must always show them even if chart future space is insufficient.

## Dashboard Synchronization

Timeline and dashboard must consume the same visible indices.

If a filter hides USD, USD events disappear from both dashboard and timeline.

## Render Fingerprint

Each event visual should have a fingerprint:

```text
event.id + event.time_broker + impact + title + visibility + selected theme
```

If fingerprint did not change, avoid recreating object.

## Cleanup Strategy

On deinit:

```text
delete GT_DASH_*
delete GT_LINE_*
delete GT_LABEL_*
delete GT_TL_*
delete GT_DIAG_*
```

On rerender:

- update existing objects;
- hide or delete stale objects owned by the module;
- never delete user-drawn objects.

## Visual Hierarchy

| Priority | Element |
|---:|---|
| 1 | next high-impact event |
| 2 | high-impact vertical lines |
| 3 | dashboard rows |
| 4 | bottom timeline markers |
| 5 | medium/low events |
| 6 | diagnostics |

## Acceptance Gate

Rendering architecture is accepted when:

- dashboard and timeline update from same filter state;
- future events are visible before chart reaches them;
- object names are deterministic;
- cleanup leaves no ghost objects;
- filter toggles do not cause full chart flicker;
- labels remain readable on dense news days.
