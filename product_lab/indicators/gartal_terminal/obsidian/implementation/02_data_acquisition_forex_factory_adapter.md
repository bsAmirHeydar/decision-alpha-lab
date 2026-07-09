---
type: implementation-phase
phase: 02
product: gartal terminal
status: planned
language: en
---

# Phase 02 — Data Acquisition & Forex Factory Adapter

## Objective

Build the source acquisition layer as a replaceable adapter. The product should be able to start with Forex Factory-style direct acquisition while remaining ready for a future API bridge, local JSON feed, or licensed data provider.

## Adapter Doctrine

The adapter must not know anything about dashboard rows, chart objects, alert states, or visual colors. It only returns raw calendar payload plus metadata.

```mermaid
flowchart LR
    A[WebRequest / File / API] --> B[Source Adapter]
    B --> C[Raw Payload]
    C --> D[Parser]
    D --> E[Normalized Event Store]
```

## Source Modes

| Mode | Purpose | Status |
|---|---|---|
| `SAMPLE_DATA` | compile-safe UI development | required in v0 |
| `FOREX_FACTORY_DIRECT` | direct calendar-source adapter | target for v1 |
| `LOCAL_CACHE` | fallback when WebRequest fails | required before beta |
| `API_BRIDGE` | future paid/controlled backend | post-beta option |
| `MANUAL_INJECTION` | emergency headlines/speeches manually injected | post-beta option |

## WebRequest Requirements

MT5 requires the target URL to be allowed in platform settings. The indicator must display a clear diagnostic if WebRequest is blocked.

Dashboard diagnostic states:

- `SOURCE OK`
- `WEBREQUEST BLOCKED`
- `SOURCE EMPTY`
- `PARSER FAILED`
- `USING CACHE`
- `SAMPLE MODE`

## Implementation Tasks

- [ ] Add enum `ENUM_GARTAL_SOURCE_MODE`.
- [ ] Build `FetchCalendarRaw()` with source mode routing.
- [ ] Add request interval throttling.
- [ ] Add last fetch timestamp.
- [ ] Add raw payload size diagnostics.
- [ ] Add WebRequest error code capture.
- [ ] Add source status line to dashboard.
- [ ] Keep source URL and route parameters in one config block.
- [ ] Do not hard-code UI behavior inside source adapter.

## Forex Factory Direct Path

The direct adapter should attempt to retrieve a date-scoped calendar page/feed and pass the raw body to the parser. The parser decides whether the body is usable.

Expected adapter output:

```cpp
struct GartalRawCalendarPayload
{
   string source_name;
   string requested_url;
   string body;
   int http_status;
   int error_code;
   datetime fetched_at_server;
   bool ok;
};
```

## Breaking/Speech Event Handling

Breaking events such as unscheduled political speeches must not be forced into the normal scheduled event model unless the source provides a timestamp. The system must support:

1. scheduled speeches from the calendar
2. tentative speeches with unknown exact time
3. breaking manually injected headlines in future adapters
4. high-priority red rendering for major unscheduled events

## Acceptance Criteria

- Source mode can be switched without changing parser, UI, timeline, or alert modules.
- WebRequest-blocked state is visible to the user.
- Empty source does not crash the indicator.
- Cache fallback is possible through a raw payload contract.

## Failure Modes

| Failure | Control |
|---|---|
| Forex Factory markup changes | parser fixtures and adapter isolation |
| Source blocks request | fallback to cache/sample diagnostics |
| Too many requests | fetch interval and manual refresh button |

## Next

- [[03_time_normalization_and_broker_gmt|Phase 03 — Time Normalization & Broker GMT]]
