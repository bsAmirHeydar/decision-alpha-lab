# EXP0013 Astro Dashboard V9 - Stable In-Place Updates

This patch fixes the most important UI behavior problem:

> The dashboard was fully deleting and rebuilding all objects on every timer refresh.

That made the whole panel feel like it was resetting instead of simply updating the numbers.

## What changed

### Before

Every `OnTimer()` render did:

```text
Delete all dashboard objects
Create everything again
```

This caused:

- flicker
- full layout reset
- buttons looking like they refresh constantly
- visual instability
- unnecessary object churn

### Now

Normal timer refresh does **in-place update only**:

```text
same object names
same layout
only text / values / bars / colors update
```

Full cleanup/rebuild only happens when it is actually needed:

- EA init
- EA deinit
- chart resize/change
- user clicks a mode/layout button
- user toggles text or oscillator panel

## Practical effect

On each candle / timer refresh, the dashboard should remain visually stable.
Only the metric values, status values, bars, and small oscillator points should update.

## Why this is the right behavior

For this dashboard, the shape/layout is static most of the time.
The only dynamic part is the astro state for the current candle or live CSV window.

So the rendering model should be:

```text
layout rebuild = rare
value update   = frequent
```

This patch implements that distinction.
