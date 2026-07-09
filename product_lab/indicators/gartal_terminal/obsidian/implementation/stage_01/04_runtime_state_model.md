# Stage 01 — Runtime State Model

## Runtime struct

```text
GT_RuntimeState
├── boot_at
├── last_timer_at
├── last_calculate_at
├── last_refresh_started_at
├── last_refresh_finished_at
├── last_refresh_at
├── last_refresh_ok
├── refresh_attempts
├── broker_gmt_detected_hours
├── last_error
├── last_warning
└── last_info
```

## Why runtime state exists

Without a runtime state object, diagnostics become scattered across modules. Stage 01 centralizes operational status so the dashboard can expose health without each module drawing its own error label.

## Diagnostic levels

```text
GT_LOG_INFO
GT_LOG_WARNING
GT_LOG_ERROR
```

## Dashboard health priority

```text
last_error > last_warning > last_info > OK
```

## Refresh state

Every refresh records:

- attempt count
- start time
- finish time
- success boolean
- final source status

This becomes critical later when direct Forex Factory fetch and cache fallback are active.
