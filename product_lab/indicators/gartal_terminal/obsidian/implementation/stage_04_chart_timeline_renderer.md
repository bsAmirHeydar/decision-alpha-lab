# Stage 04 — Chart Timeline Renderer

## Purpose

Stage 04 turns the normalized event store into a chart-native visual tape. The chart must show the trader what is coming before price reaches that time region. This stage does not fetch Forex Factory data and does not implement interactive filters yet. It consumes the Stage 02 store and the Stage 03 broker-time authority.

## Hard Contract

`event.time_broker` is the only timestamp used for rendering. No renderer may recalculate source time, UTC time, or broker GMT.

## Implemented Renderer Surfaces

- Vertical event lines.
- Rotated timeline labels near the lower chart region.
- High-impact / breaking-news danger zones.
- Bottom tape panel with the next visible events.
- Renderer diagnostics in the dashboard.
- Timeline object cleanup using a dedicated namespace.

## Files

```text
mql5/include/GartalNewsChartGeometry.mqh
mql5/include/GartalNewsTimeline.mqh
mql5/include/GartalNewsInputs.mqh
mql5/include/GartalNewsTypes.mqh
mql5/include/GartalNewsDashboard.mqh
mql5/GartalTerminal.mq5
```

## Downstream Handoff

Stage 05 can now build the luxury dashboard without carrying chart-object responsibility. Stage 06 can later mutate filters and call the same redraw path.
