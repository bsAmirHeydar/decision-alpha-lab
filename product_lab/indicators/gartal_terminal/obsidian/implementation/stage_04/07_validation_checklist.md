# Stage 04 Validation Checklist

## Compile

- `GartalTerminal.mq5` opens in MetaEditor.
- No duplicate function definitions.
- `GartalNewsChartGeometry.mqh` is included before `GartalNewsTimeline.mqh`.

## Visual

- Vertical lines appear at event broker times.
- Red events have thicker lines.
- Breaking events are red and have danger zones.
- Labels are visible near the lower chart area.
- Bottom tape shows the next visible events.
- Dashboard shows timeline render counters.

## Runtime

- Changing chart scale does not duplicate objects.
- Changing timeframe does not leave stale timeline objects.
- `InpTimelineMaxEvents` caps object count.
- `InpShowReleasedTimelineObjects=false` hides old released/expired event objects.
