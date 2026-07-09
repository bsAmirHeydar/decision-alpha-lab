# 02 — Broker GMT Detection

## Detection method

The terminal compares the broker/server clock against GMT:

```text
raw_delta = TimeCurrent() - TimeGMT()
detected_offset = snap(raw_delta to nearest minute)
```

The engine records:

- `runtime.time_snapshot_server`
- `runtime.time_snapshot_gmt`
- `runtime.time_snapshot_local`
- `runtime.server_gmt_raw_delta_seconds`
- `runtime.broker_gmt_detected_seconds`
- `runtime.broker_gmt_confidence`

## Modes

| Mode | Value | Behavior |
|---|---:|---|
| Auto | 0 | Use detected broker GMT offset |
| Manual | 1 | Use user-provided offset |
| Hybrid | 2 | Use auto when confidence is acceptable, otherwise manual |

## Confidence

Confidence is based on how cleanly the raw delta snaps to a minute boundary:

```text
<= 5 sec error   -> 100
<= 30 sec error  -> 85
<= 90 sec error  -> 60
else             -> 35
```

This is intentionally simple and compile-safe for MT5. Later releases can extend this to session probes and broker-calendar checks.

## Product default

Default is Auto, but the dashboard exposes the detected/effective GMT so a user can override manually if a broker has abnormal server behavior.
