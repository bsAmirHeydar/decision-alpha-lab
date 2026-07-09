# 01 — Time Authority Contract

## Rule

The system has exactly one render authority:

```text
event.time_broker
```

No dashboard, timeline, alert, or vertical-line module may independently convert source time or UTC time. All conversion happens once, during event insertion/finalization.

## Stored timestamps

| Field | Meaning | Consumer |
|---|---|---|
| `time_source` | Time as interpreted from source/calendar context | parser audit, debug panel |
| `time_utc` | Canonical neutral timestamp | cache, future API bridges |
| `time_broker` | Final chart/render/alert time | all product UX |
| `day_start_broker` | Broker-day midnight | grouping, labels, day offsets |

## Why this matters

Economic calendar products fail commercially when news lines appear one hour early/late. Traders do not forgive time errors. This stage makes every downstream module dependent on a single normalized broker-time contract.

## Prohibited pattern

```text
parser -> dashboard time conversion
parser -> alert time conversion
parser -> timeline time conversion
```

## Required pattern

```text
parser/sample/source -> event insertion -> time engine -> event.time_broker -> all renderers
```
