---
type: implementation-phase
phase: 07
product: gartal terminal
status: planned
language: en
---

# Phase 07 — Alert Engine Implementation

## Objective

Build a staged alert system that notifies the trader before and during news events without spamming repeated alerts on every tick.

## Alert Channels

| Channel | Required |
|---|---:|
| MT5 Popup Alert | yes |
| Sound Alert | yes |
| Push Notification | yes |
| Email Alert | optional/user-enabled |
| Chart Flash/Highlight | yes |
| Dashboard Badge | yes |

## Alert Stages

| Stage | Default |
|---|---:|
| 60 minutes before | off |
| 30 minutes before | on |
| 15 minutes before | on |
| 5 minutes before | on |
| 1 minute before | off |
| At release | on |
| Actual value updated | optional/future |
| Breaking event received | on |

## Alert State Doctrine

Every alert must have a unique key:

```text
<event_id>::<alert_stage>::<broker_time>
```

Once fired, it must not fire again unless:

- event is revised
- indicator is reset and persisted state is intentionally cleared
- user manually resets alert state

## Implementation Tasks

- [ ] Define `ENUM_GARTAL_ALERT_STAGE`.
- [ ] Define per-event alert fired flags.
- [ ] Build `EvaluateAlertStages(event, now_broker_time)`.
- [ ] Build `DispatchAlert(event, stage, channel_config)`.
- [ ] Build dedupe store.
- [ ] Add dashboard alert master switch.
- [ ] Add channel toggles in dashboard.
- [ ] Add per-stage toggles in inputs.
- [ ] Add cooldown control.
- [ ] Add alert test button.
- [ ] Add alert log in debug mode.

## Alert Message Format

```text
gartal terminal | HIGH USD News in 15m
Event: Non-Farm Payrolls
Time: 16:30 Broker
Forecast: 180K | Previous: 175K
```

For breaking events:

```text
gartal terminal | BREAKING RED EVENT
Event: Unscheduled speech / political headline
Currency: USD
Time: now / source time
```

## Acceptance Criteria

- Alerts fire once per enabled stage.
- User can enable/disable alerts from dashboard.
- Alert settings survive normal chart refresh when state persistence is enabled.
- Disabled event types do not produce alerts.
- High-impact events can have stricter default alert behavior than low-impact events.

## Failure Modes

| Failure | Control |
|---|---|
| Alert spam on every tick | stage dedupe keys |
| Alert for hidden event | alert engine reads visible event set only |
| User misses source failure | separate source-failure dashboard warning, not news alert spam |
| Push/email not configured in MT5 | diagnostic warning in dashboard/footer |

## Next

- [[08_cache_resilience_and_failover|Phase 08 — Cache, Resilience & Failover]]
