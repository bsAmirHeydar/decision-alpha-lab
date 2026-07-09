# STAGE 04 — Chart Timeline Renderer Specification

## Objective

Implement the first production-grade chart visualization layer for `gartal terminal`. The renderer converts the canonical broker-time event store into visible MT5 chart objects.

## Non-Goals

- No real Forex Factory parsing.
- No runtime filter toggles.
- No luxury dashboard redesign.
- No final collision engine.

## Inputs Added

```text
InpShowEventLabels
InpShowBottomTape
InpShowDangerZones
InpShowTimelineTooltips
InpShowReleasedTimelineObjects
InpShowTimelineDebug
InpTimelineCompactTitles
InpTimelineMaxEvents
InpTimelineLabelRows
InpTimelineBottomY
InpTimelineProjectionMinutes
InpPreNewsZoneMinutes
InpPostNewsZoneMinutes
```

## Core Modules

### GartalNewsChartGeometry.mqh

Owns chart price range helpers, timeline label price rows, danger-zone price bounds, and projection horizon helpers.

### GartalNewsTimeline.mqh

Owns all chart timeline rendering:

- cleanup
- vertical event lines
- lower chart event labels
- red/breaking danger zones
- bottom tape
- runtime render diagnostics

## Object Namespaces

```text
GT_TL_        chart-time objects
GT_TIMELINE_  bottom tape panel
GT_DASH_      dashboard
```

## Render Authority

Only `event.time_broker` may be used for chart x-position.

## Success Criteria

- Event lines align with broker-time event values.
- Red/breaking events are visually dominant.
- Future events render within the projection horizon.
- Cleanup prevents stale objects on refresh/timeframe change.
- Dashboard reports renderer counters.
