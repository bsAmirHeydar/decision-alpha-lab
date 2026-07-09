# Dashboard Contract

The dashboard is a renderer, not a source of truth. It receives:

```text
GT_Config       visual and behavior settings
GT_NewsStore    canonical event store
GT_FilterState  current visible universe
GT_RuntimeState diagnostics and render counters
```

It outputs MT5 objects under the `GT_DASH_` namespace.

## Hard Rule

The dashboard must never derive event time from source text. Only `event.time_broker` is display-authoritative.

## Stage 05 Boundary

`GT_HandleDashboardClick()` remains a no-op. Runtime mutation begins in Stage 06.
