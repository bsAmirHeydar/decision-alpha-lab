---
type: implementation-phase
phase: 06
product: gartal terminal
status: planned
language: en
---

# Phase 06 — Chart Timeline Renderer

## Objective

Render all visible upcoming news directly on the chart timeline, including vertical event lines and a bottom forward strip that shows what is coming until the end of the selected date range.

The trader should be able to see future risk zones before price reaches them visually.

## Renderer Responsibilities

| Element | Purpose |
|---|---|
| Vertical event line | exact event time on the chart |
| Event label | currency, impact, short title |
| Bottom timeline marker | future news schedule below price action |
| Pre/post news zone | optional shaded risk window |
| Next event marker | visually stronger marker for nearest high-priority event |

## Chart Object Model

Object names should be deterministic:

```text
GT_LINE_<event_id>
GT_LABEL_<event_id>
GT_STRIP_<event_id>
GT_ZONE_PRE_<event_id>
GT_ZONE_POST_<event_id>
```

## Timeline Rules

- Future events must be drawn ahead of current price action.
- Past events are either dimmed or removed depending on input.
- High-impact events get strongest line treatment.
- Medium events get secondary line treatment.
- Low events are hidden by default.
- Tentative events use dashed or visually uncertain treatment.
- Breaking events use urgent red treatment.

## Implementation Tasks

- [ ] Build `DrawEventLine(event)`.
- [ ] Build `DrawEventLabel(event)`.
- [ ] Build `DrawBottomTimelineMarker(event)`.
- [ ] Build `DrawPrePostRiskWindow(event)`.
- [ ] Build `DeleteStaleTimelineObjects()`.
- [ ] Build object cap protection.
- [ ] Add input: show/hide vertical lines.
- [ ] Add input: show/hide bottom timeline strip.
- [ ] Add input: risk window minutes before/after.
- [ ] Add input: show past events.
- [ ] Add visual priority sorting for overlapping labels.

## Label Collision Doctrine

When multiple events share the same time:

1. group by event time
2. show high-impact currencies first
3. compress labels into stacked badges
4. avoid dumping long titles directly on the chart
5. full details remain in the dashboard table

## Acceptance Criteria

- Upcoming events are drawn at correct broker chart time.
- Bottom strip shows all selected events until end of selected range.
- Multiple events at same time do not create unreadable overlap.
- User can disable timeline strip or event lines separately.
- Objects are removed cleanly on deinit/timeframe change.

## Failure Modes

| Failure | Control |
|---|---|
| Object leftovers after timeframe change | strict prefix cleanup on init/deinit |
| Lines drawn one hour wrong | use broker_time only, never source_time |
| Too many labels | cap labels + dashboard full table |
| Chart clutter | compact labels + filters + UI density |

## Next

- [[07_alert_engine_implementation|Phase 07 — Alert Engine Implementation]]
