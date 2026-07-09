# Stage 07 — Alert Engine + Alert State Machine

## Purpose

Stage 07 turns `gartal terminal` from a visual news terminal into an operational event-warning system. The module must warn the trader before relevant macro events, at release time, after actual values become available, and when unscheduled/breaking red events enter the event tape.

The implementation must be deterministic:

- one event + one alert stage = one alert key;
- duplicate keys never fire twice;
- runtime dashboard filters can suppress alerts when enabled;
- alert delivery is separated from alert eligibility;
- the event store remains read-only during alert processing.

## Files touched

```text
mql5/GartalTerminal.mq5
mql5/include/GartalNewsTypes.mqh
mql5/include/GartalNewsInputs.mqh
mql5/include/GartalNewsDiagnostics.mqh
mql5/include/GartalNewsFilters.mqh
mql5/include/GartalNewsDashboard.mqh
mql5/include/GartalNewsAlerts.mqh
```

## Runtime lifecycle

```text
OnTimer
  ├─ refresh calendar when due
  ├─ update event statuses
  ├─ update store metrics
  ├─ process alerts
  └─ update dashboard countdowns
```

Alert processing happens after store metrics so the engine sees the same filtered truth as the dashboard and timeline.

## Alert stages

```text
PRE_60M
PRE_30M
PRE_15M
PRE_5M
PRE_1M
RELEASE
ACTUAL
BREAKING
```

Each stage creates a distinct key:

```text
event.id + "_" + stage
```

This makes the engine duplicate-safe even when `OnTimer` runs many times inside the same minute.

## Non-overlap pre-alert bands

The engine intentionally avoids the common bug where starting the indicator five minutes before an event fires every missed threshold at once.

```text
60m alert: remaining <= 60m and remaining > 30m
30m alert: remaining <= 30m and remaining > 15m
15m alert: remaining <= 15m and remaining > 5m
5m alert:  remaining <= 5m  and remaining > 1m
1m alert:  remaining <= 1m  and remaining >= 0
```

This is better for a commercial terminal because it prevents alert spam.

## Release alert

Release alerts are time-window based:

```text
now >= event.time_broker
now <= event.time_broker + InpAlertReleaseWindowSeconds
```

Default release window: `90` seconds.

## Actual alert

The actual-value alert fires when:

```text
InpAlertAfterActual = true
event.is_released = true OR event.actual is not empty
now >= event.time_broker
```

In Stage 07 this is mostly visible through sample data. In Stage 08/09 it becomes important when the Forex Factory adapter updates `actual`, `forecast`, and `previous` values after the release.

## Breaking alert

Breaking alerts fire immediately when an event is marked as `is_breaking=true` and still belongs to the active/recent window. This supports unscheduled red events such as presidential remarks, emergency central-bank statements, surprise press conferences, or geopolitical headlines once the real source adapter is connected.

## Runtime filter respect

`InpAlertRespectRuntimeFilters=true` means:

```text
if dashboard filters hide the event, the alert engine ignores it.
```

This connects Stage 06 directly to Stage 07. A user can click `ALERTS OFF` on the dashboard to pause alerts without changing the indicator inputs.

## Alert diagnostics

Runtime state now tracks:

```text
alert_scan_count
alert_last_scanned_events
alert_last_visible_candidates
alert_last_sent_count
alert_last_suppressed_count
alert_last_scan_at
alert_last_sent_at
alert_last_stage
alert_last_event_id
alert_last_message
alert_last_summary
```

The dashboard health/debug line uses these fields.

## Handoff

Stage 07 is complete when:

- the indicator compiles;
- alert state initializes on `OnInit`;
- timer-driven alert scans run without modifying the event store;
- dashboard `ALERTS` button toggles `filters.alerts_enabled`;
- duplicate keys do not fire twice;
- alert diagnostics are visible in logs/debug surfaces;
- sample breaking event can trigger a breaking watch alert.

Next stage: [[../stage_08_forex_factory_client_html_parser|Stage 08 — Forex Factory Client + HTML Parser]].
