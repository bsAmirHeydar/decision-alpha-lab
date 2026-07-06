# Chart Change Must Rebuild Hook View

A timeframe or symbol change changes the chart identity. Hook visual state must be treated as stale.

Policy:

```text
chart identity changed
=> cleanup Hook objects
=> reset runtime redraw state
=> rebuild from the new symbol/period timebase
```

The renderer must not rely on old object state, old bar-time throttle state, or old label caches after a chart identity change.

This is a runtime hygiene policy. It does not modify Hook semantic validity.
