# Stage 01 — Core Contract

## Contract statement

The indicator must expose a stable internal runtime where each future feature can be inserted behind a narrow function boundary.

## Required global state

```text
GT_Config       g_config
GT_RuntimeState g_runtime
GT_NewsStore    g_store
GT_FilterState  g_filters
GT_AlertState   g_alerts
```

## Core invariants

1. `g_config` is loaded once on `OnInit`.
2. `g_store` is reset before every refresh.
3. `g_runtime` records diagnostic state instead of scattering raw `Print()` calls.
4. `g_filters` mirrors initial input settings and later becomes the dashboard runtime filter state.
5. `g_alerts` remembers sent alert keys so repeated timer ticks do not spam the user.

## Refresh contract

```text
GT_RefreshCalendar(first_load)
  → choose source mode
  → fetch/load raw data if needed
  → parse/load events
  → sort events
  → mark relevance against current symbol
  → update statuses
  → redraw dashboard/timeline/lines
```

## Renderer contract

All renderers must be idempotent:

- same input state can be rendered repeatedly
- object names are deterministic
- object cleanup is prefix-based
- no renderer owns source/parsing logic

## Error contract

Hard initialization failures set:

```text
runtime.last_error
```

Recoverable failures set:

```text
runtime.last_warning
```

The dashboard reads both through `GT_RuntimeStatusText()`.
