# Renderer Contract

## Authority

The renderer reads only these event fields:

```text
time_broker
currency
impact
title
status
kind
actual / forecast / previous
```

It does not parse data. It does not normalize time. It does not own filtering logic. It only asks `GT_EventPassesFilters()` and `GT_EventInsideProjection()`.

## Render Order

1. Clear old `GT_TL_` objects.
2. Iterate sorted store events.
3. Skip events outside filters or projection horizon.
4. Render danger zone for high/breaking events.
5. Render vertical line.
6. Render rotated event label.
7. Render bottom tape.
8. Update runtime diagnostics.
