# Handoff to Stage 07

Stage 07 implements the alert engine.

The important contract from Stage 06:

```mql5
GT_EventPassesFilters(ev, filters)
```

Alerts must call this before firing. If the user has hidden USD or disabled red events, the alert engine must not notify on those hidden events.

Stage 07 should also add dashboard controls for alert enablement only after the base alert state machine is stable.
