# Stage 01 — Module Boundaries

## `GartalTerminal.mq5`

Role: orchestration only.

Allowed:

- lifecycle functions
- top-level refresh route
- redraw route

Forbidden:

- parsing details
- object styling details
- alert threshold details
- source-specific HTML logic

## `GartalNewsTypes.mqh`

Role: shared structs and constants.

Contains:

- impact constants
- data mode constants
- event status constants
- log constants
- config/store/filter/alert/runtime structs

## `GartalNewsUtils.mqh`

Role: safe helper layer.

Important wrappers:

- `GT_ToUpper`
- `GT_ToLower`
- `GT_Trim`
- `GT_CsvContains`
- `GT_SafeObjectName`

## `GartalNewsInputs.mqh`

Role: input-to-config mapping.

Rules:

- clamp risky numeric inputs
- convert currency CSV to uppercase
- default to sample data
- derive `data_mode`

## `GartalNewsTime.mqh`

Role: all broker/source/UTC conversion.

Stage 01 includes:

- broker GMT detection
- UTC ↔ broker conversion
- source → broker conversion
- date-window check
- event status update

## `GartalNewsParser.mqh`

Role: event-store construction.

Stage 01 includes sample data only. Direct Forex Factory parsing is deliberately blocked with a warning.

## `GartalNewsDashboard.mqh`

Role: fixed dashboard renderer.

Stage 01 renders:

- shell
- status
- next event
- event rows

## `GartalNewsTimeline.mqh`

Role: chart-time visualization.

Stage 01 renders:

- vertical event lines
- bottom timeline shell

## `GartalNewsAlerts.mqh`

Role: alert state and dispatch.

Stage 01 includes:

- alert key memory
- threshold dispatch
- release-time dispatch
