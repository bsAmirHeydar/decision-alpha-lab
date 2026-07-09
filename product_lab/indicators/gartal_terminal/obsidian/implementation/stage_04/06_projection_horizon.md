# Projection Horizon

## Purpose

The user asked for news to appear ahead of the current chart area. Stage 04 introduces `InpTimelineProjectionMinutes` as the render horizon from broker now.

## Default

```text
720 minutes = 12 hours
```

## Behavior

Events beyond the horizon are not rendered as chart objects. This prevents the indicator from creating excessive future objects on high-density calendar days.
