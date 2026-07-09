# Stage 01 — MQL5 Lifecycle Map

## OnInit

`OnInit` is the only place where boot-critical operations are allowed.

```text
GT_ResetRuntime
GT_ResetStore
GT_LoadConfig
GT_InitFilterState
GT_InitAlertState
GT_ClearObjects
GT_ValidateConfig
GT_NormalizeConfigTime
GT_RenderShell
EventSetTimer
GT_RefreshCalendar(true)
```

## OnTimer

Timer owns runtime progression:

```text
if refresh due:
  GT_RefreshCalendar(false)

GT_ProcessAlerts
GT_UpdateCountdowns
```

## OnCalculate

`OnCalculate` is intentionally minimal. The indicator is not price-calculation heavy.

Allowed in Stage 01:

```text
runtime.last_calculate_at = TimeCurrent()
return rates_total
```

Not allowed in Stage 01:

- WebRequest
- full redraw
- parser execution
- expensive object scans

## OnChartEvent

Stage 01 wires the event route but does not activate dashboard toggles yet.

```text
CHARTEVENT_OBJECT_CLICK → GT_HandleDashboardClick
CHARTEVENT_CHART_CHANGE → GT_RedrawAll
```

## OnDeinit

On deinit:

```text
EventKillTimer
optional prefix cleanup
```

No file writing and no WebRequest is allowed in deinit.
