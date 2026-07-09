---
type: architecture
product: gartal terminal
status: active
language: en
tags:
  - mql5
  - contracts
  - module-boundaries
---

# 02 — MQL5 Module Contracts

## Module List

The current scaffold must evolve into this final module map:

```text
mql5/
├── GartalTerminal.mq5
└── include/
    ├── GartalNewsTypes.mqh
    ├── GartalNewsInputs.mqh
    ├── GartalNewsCalendarClient.mqh
    ├── GartalNewsParser.mqh
    ├── GartalNewsTime.mqh
    ├── GartalNewsStore.mqh
    ├── GartalNewsFilters.mqh
    ├── GartalNewsDashboard.mqh
    ├── GartalNewsTimeline.mqh
    ├── GartalNewsAlerts.mqh
    ├── GartalNewsCache.mqh
    ├── GartalNewsDiagnostics.mqh
    └── GartalNewsTheme.mqh
```

Some files may not exist yet. They are introduced as implementation phases become active.

## `GartalTerminal.mq5`

### Responsibility

Orchestration only.

### Owns

- lifecycle functions;
- timer setup;
- module call order;
- high-level error recovery;
- global state instances.

### Must Not Own

- HTML parsing;
- dashboard layout details;
- object creation loops;
- alert duplicate keys;
- source-specific impact parsing.

### Contract

```cpp
int OnInit();
void OnDeinit(const int reason);
int OnCalculate(...);
void OnTimer();
void OnChartEvent(const int id, const long &lparam, const double &dparam, const string &sparam);
```

## `GartalNewsTypes.mqh`

### Responsibility

Canonical enums, structs, constants, and object prefixes.

### Required Types

```cpp
enum GT_Impact
{
   GT_IMPACT_NONE = 0,
   GT_IMPACT_LOW = 1,
   GT_IMPACT_MEDIUM = 2,
   GT_IMPACT_HIGH = 3,
   GT_IMPACT_HOLIDAY = 4
};

enum GT_SourceStatus
{
   GT_SOURCE_IDLE = 0,
   GT_SOURCE_OK = 1,
   GT_SOURCE_HTTP_ERROR = 2,
   GT_SOURCE_PARSE_ERROR = 3,
   GT_SOURCE_CACHE = 4,
   GT_SOURCE_SAMPLE = 5
};

enum GT_AlertStage
{
   GT_ALERT_STAGE_60M = 60,
   GT_ALERT_STAGE_30M = 30,
   GT_ALERT_STAGE_15M = 15,
   GT_ALERT_STAGE_5M = 5,
   GT_ALERT_STAGE_1M = 1,
   GT_ALERT_STAGE_RELEASE = 0,
   GT_ALERT_STAGE_ACTUAL = -1
};
```

## `GartalNewsInputs.mqh`

### Responsibility

Convert MT5 inputs into a canonical runtime config.

### Output

```cpp
bool GT_LoadConfig(GT_Config &config);
```

### Input Philosophy

Inputs are static startup defaults. The dashboard is runtime control.

Dashboard clicks must update `GT_FilterState`, not the original MQL5 `input` variables.

## `GartalNewsCalendarClient.mqh`

### Responsibility

Fetch raw source payload.

### Contract

```cpp
bool GT_FetchCalendarPayload(const GT_Config &config, string &payload, GT_SourceStatus &status, string &error_message);
```

### Allowed Internals

- `WebRequest`;
- URL building;
- timeout;
- request headers;
- cache loading when enabled;
- sample payload when sample mode is enabled.

### Forbidden Internals

- parsing event rows;
- assigning chart colors;
- dashboard changes;
- alert dispatching.

## `GartalNewsParser.mqh`

### Responsibility

Convert raw source payload into canonical event structs.

### Contract

```cpp
bool GT_ParseCalendarPayload(const string payload, GT_NewsStore &store, string &error_message);
```

### Output Rule

Parser sets `source_time`, `currency`, `impact`, `title`, `actual`, `forecast`, `previous`, and semantic flags.

It does not set final broker-time unless source time contains enough timezone context. Broker-time is owned by `GartalNewsTime.mqh`.

## `GartalNewsTime.mqh`

### Responsibility

Normalize event time.

### Contract

```cpp
int GT_DetectBrokerGmtOffsetMinutes();
bool GT_NormalizeEventTimes(GT_NewsStore &store, const GT_Config &config, string &error_message);
```

### Rules

- source time must become UTC first;
- UTC must become broker time second;
- dashboard display must use broker time by default;
- manual GMT offset must override auto detection when enabled.

## `GartalNewsStore.mqh`

### Responsibility

Canonical event storage and deduplication.

### Contract

```cpp
void GT_StoreClear(GT_NewsStore &store);
bool GT_StoreAddOrUpdate(GT_NewsStore &store, const GT_NewsEvent &event);
void GT_StoreSortByBrokerTime(GT_NewsStore &store);
```

### Dedup Key

```text
YYYYMMDD-HHMM-CURRENCY-IMPACT-TITLE_HASH
```

## `GartalNewsFilters.mqh`

### Responsibility

Compute visible events from canonical store and runtime filter state.

### Contract

```cpp
int GT_BuildVisibleEventIndices(const GT_NewsStore &store, const GT_Config &config, const GT_FilterState &filters, int &indices[]);
```

### Forbidden

- deleting events from store;
- mutating source fields;
- drawing UI.

## `GartalNewsDashboard.mqh`

### Responsibility

Draw the dashboard and process dashboard clicks.

### Contract

```cpp
void GT_RenderDashboard(const GT_NewsStore &store, const int &visible_indices[], const int visible_count, const GT_Config &config, const GT_FilterState &filters);
bool GT_HandleDashboardClick(const string object_name, GT_FilterState &filters);
```

### Object Ownership

All objects must start with:

```text
GT_DASH_
```

## `GartalNewsTimeline.mqh`

### Responsibility

Draw chart lines and future bottom timeline strip.

### Contract

```cpp
void GT_RenderTimeline(const GT_NewsStore &store, const int &visible_indices[], const int visible_count, const GT_Config &config);
```

### Object Ownership

All objects must start with:

```text
GT_LINE_
GT_TL_
```

## `GartalNewsAlerts.mqh`

### Responsibility

Process alert stages and dispatch configured channels once.

### Contract

```cpp
void GT_ProcessAlerts(const GT_NewsStore &store, const int &visible_indices[], const int visible_count, const GT_Config &config, GT_AlertState &state);
```

### Required Idempotency Key

```text
EVENT_ID|STAGE|CHANNEL
```

## `GartalNewsCache.mqh`

### Responsibility

Persist last valid source payload and/or normalized events.

### Contract

```cpp
bool GT_SaveCache(const string cache_key, const string payload);
bool GT_LoadCache(const string cache_key, string &payload);
```

## `GartalNewsDiagnostics.mqh`

### Responsibility

Expose source, parse, time, filter, render, and alert state in a compact debug block.

### Contract

```cpp
void GT_RenderDiagnostics(const GT_NewsStore &store, const GT_Config &config, const string status_line);
```

## Dependency Matrix

| Module | Can Depend On |
|---|---|
| Terminal | all modules |
| Types | none |
| Inputs | Types |
| Calendar Client | Types, Cache |
| Parser | Types |
| Time | Types |
| Store | Types |
| Filters | Types, Store |
| Dashboard | Types, Theme |
| Timeline | Types, Theme |
| Alerts | Types |
| Cache | Types |
| Diagnostics | Types, Theme |
| Theme | Types |
