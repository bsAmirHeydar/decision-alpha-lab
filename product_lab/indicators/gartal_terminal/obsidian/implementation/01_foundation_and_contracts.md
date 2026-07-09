---
type: implementation-phase
phase: 01
product: gartal terminal
status: planned
language: en
---

# Phase 01 — Foundation & Contracts

## Objective

Create a compile-safe architecture where every future subsystem has a stable contract before real source parsing or heavy UI work begins.

This phase prevents the indicator from becoming a monolithic MQL5 file. The target is a clean internal API between inputs, calendar events, filters, dashboard rendering, timeline rendering, and alerts.

## Modules

| Module | Responsibility |
|---|---|
| `GartalNewsTypes.mqh` | canonical event structs, enums, UI state structs |
| `GartalNewsInputs.mqh` | input config and dashboard-editable runtime config |
| `GartalNewsCalendarClient.mqh` | source fetching contract |
| `GartalNewsParser.mqh` | raw payload to normalized event conversion |
| `GartalNewsDashboard.mqh` | dashboard object creation/update |
| `GartalNewsTimeline.mqh` | chart event lines and bottom timeline strip |
| `GartalNewsAlerts.mqh` | alert stage state and dispatch |
| `GartalTerminal.mq5` | orchestration only |

## Required Data Contracts

### Event Struct

```cpp
struct GartalNewsEvent
{
   string id;
   datetime source_time;
   datetime utc_time;
   datetime broker_time;
   string currency;
   string impact;
   string title;
   string actual;
   string forecast;
   string previous;
   bool is_speech;
   bool is_holiday;
   bool is_tentative;
   bool is_breaking;
   bool is_revised;
};
```

### Runtime Config

The runtime config must support both MT5 inputs and dashboard toggles.

```cpp
struct GartalRuntimeConfig
{
   bool show_usd;
   bool show_eur;
   bool show_gbp;
   bool show_jpy;
   bool show_chf;
   bool show_cad;
   bool show_aud;
   bool show_nzd;
   bool show_cny;

   bool show_low;
   bool show_medium;
   bool show_high;
   bool show_speeches;
   bool show_holidays;
   bool show_tentative;
   bool show_breaking;

   int days_back;
   int days_forward;
   int broker_gmt_offset_minutes;
   bool auto_detect_broker_gmt;
};
```

## Implementation Tasks

- [ ] Define canonical enums for impact, source status, alert stage, and UI density.
- [ ] Define canonical structs for event, event array, runtime config, dashboard state, and alert state.
- [ ] Keep all object name prefixes under one constant: `GT_`.
- [ ] Make the indicator compile with `InpUseSampleData = true`.
- [ ] Add a debug panel line that shows: event count, source mode, broker GMT mode, last fetch time.
- [ ] Ensure all modules are imported from `mql5/include/` and the main `.mq5` is only an orchestrator.

## Acceptance Criteria

- Indicator compiles in MetaEditor without network access.
- Sample data renders through the same pipeline as real data will use later.
- No renderer reads raw source payload directly.
- No alert logic reads raw source payload directly.
- No module directly manipulates another module's private state.

## Failure Modes

| Failure | Fix |
|---|---|
| Main `.mq5` starts containing parser/UI/alert logic | move logic into corresponding include module |
| Source adapter returns UI-specific fields | keep adapter raw and parser normalized |
| Dashboard changes do not affect timeline | ensure both read from one runtime config object |

## Next

- [[02_data_acquisition_forex_factory_adapter|Phase 02 — Data Acquisition & Forex Factory Adapter]]
