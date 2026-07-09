# Stage 01 — Compile-Safe Core Skeleton

> Product: [[gartal terminal]]  
> Implementation layer: MT5 / MQL5  
> Stage status: **Code-first foundation**  
> Primary output: a deterministic indicator skeleton that compiles, boots, renders a minimal terminal, and isolates every future subsystem behind stable contracts.

## 1. Purpose

Stage 01 does **not** try to solve the Forex Factory parser. It establishes the internal product spine:

- MQL5 indicator lifecycle
- config loader
- runtime state
- event store
- sample data pipeline
- dashboard shell
- timeline shell
- vertical-line renderer
- alert state memory
- direct-source placeholder
- cache placeholder
- diagnostic log contract

The goal is simple: before the project becomes visually rich or source-dependent, the core must be able to compile and behave predictably.

## 2. Non-goals

Stage 01 explicitly does **not** include:

- production Forex Factory HTML parsing
- runtime dashboard toggles
- luxury final UI
- draggable dashboard
- breaking-news feed integration
- release packaging
- licensing enforcement
- performance hardening

Those are later stages. Stage 01 only guarantees that the project has a stable execution skeleton.

## 3. Stage 01 file map

```text
mql5/
├── GartalTerminal.mq5
└── include/
    ├── GartalNewsTypes.mqh
    ├── GartalNewsUtils.mqh
    ├── GartalNewsInputs.mqh
    ├── GartalNewsTime.mqh
    ├── GartalNewsDiagnostics.mqh
    ├── GartalNewsCalendarClient.mqh
    ├── GartalNewsParser.mqh
    ├── GartalNewsDashboard.mqh
    ├── GartalNewsTimeline.mqh
    └── GartalNewsAlerts.mqh
```

## 4. Runtime sequence

```text
OnInit
  → Reset runtime/store
  → Load config from inputs
  → Initialize filter state
  → Initialize alert state
  → Clear old chart objects
  → Validate config
  → Detect broker GMT if enabled
  → Render shell
  → Start timer
  → Refresh calendar once

OnTimer
  → Refresh calendar if refresh interval is due
  → Process alert thresholds
  → Update countdown placeholders

OnChartEvent
  → route object click pipeline
  → redraw on chart changes

OnDeinit
  → kill timer
  → optionally clear all GT_* objects
```

## 5. Architecture doctrine

Stage 01 uses a strict boundary rule:

> The top-level indicator may orchestrate modules, but it must not contain business logic.

That means:

- parsing belongs to `GartalNewsParser.mqh`
- source fetch belongs to `GartalNewsCalendarClient.mqh`
- time normalization belongs to `GartalNewsTime.mqh`
- object rendering belongs to dashboard/timeline modules
- alert state belongs to `GartalNewsAlerts.mqh`
- diagnostics belong to `GartalNewsDiagnostics.mqh`

## 6. Compile-safe design decisions

### 6.1 String normalization wrappers

MQL5 string functions such as `StringToUpper` and `StringToLower` are not treated like pure return-value helpers in this codebase. Stage 01 adds wrappers:

```text
GT_ToUpper(value)
GT_ToLower(value)
GT_Trim(value)
```

This prevents compile errors and avoids inconsistent string mutation patterns.

### 6.2 Sample-data first

`InpUseSampleData=true` is the Stage 01 default. The indicator can render and test time/chart behavior without waiting for the Forex Factory adapter.

### 6.3 Object prefix discipline

All chart objects use the configurable prefix:

```text
GT_
```

The cleanup engine only deletes objects that start with this prefix.

### 6.4 Timer-driven runtime

`OnCalculate` remains lightweight. Refresh, alerts, and dashboard updates are timer-driven.

## 7. Acceptance criteria

Stage 01 is complete when:

- the indicator compiles without undefined identifiers
- the indicator boots on a chart
- old `GT_` objects are cleared on initialization
- sample events are loaded into `GT_NewsStore`
- dashboard shows product name, source status, GMT, count, and event rows
- vertical lines are drawn for visible sample events
- timeline shell shows upcoming event count
- alert state exists without duplicate-send risk
- Forex Factory direct source is present only as a placeholder path

## 8. Next stage handoff

Next: [[00_STAGE_02_INDEX|Stage 02 — News Event Data Model + Sample Data Pipeline]]

Stage 02 should expand the event model and sample data layer into a richer simulation environment before real source integration.
