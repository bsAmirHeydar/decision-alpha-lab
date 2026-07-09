---
type: architecture
product: gartal terminal
status: active
language: en
tags:
  - cache
  - resilience
  - error-handling
  - webrequest
---

# 09 — Error, Cache & Resilience Architecture

## Goal

The terminal must degrade gracefully when the data source fails.

A sellable product cannot silently show empty news without explaining whether the day is truly empty or the source failed.

## Source Status Model

Canonical status:

| Status | Meaning | UI Message |
|---|---|---|
| `GT_SOURCE_OK` | live source fetch succeeded | Live |
| `GT_SOURCE_SAMPLE` | sample mode | Sample Data |
| `GT_SOURCE_CACHE` | using last valid cache | Cache |
| `GT_SOURCE_HTTP_ERROR` | WebRequest/network failed | Source Error |
| `GT_SOURCE_PARSE_ERROR` | payload received but parser failed | Parser Error |
| `GT_SOURCE_EMPTY` | source parsed but no events found | No Events |

## WebRequest Failure Handling

Common MT5 failure causes:

- URL not whitelisted in MT5 settings;
- network timeout;
- blocked by broker/VPS environment;
- source response changed;
- TLS/HTTP restriction.

Required behavior:

1. show dashboard diagnostic;
2. attempt cache fallback if enabled;
3. keep previous render if safer than blanking;
4. avoid alerting from stale data unless allowed.

## Cache Policy

Cache should store:

- raw payload;
- fetch timestamp;
- source URL;
- payload hash;
- optionally normalized event JSON/CSV later.

V1 file naming:

```text
Files/gartal_terminal/cache/calendar_{YYYYMMDD}_{source_hash}.txt
```

## Cache Freshness

| Cache Age | Behavior |
|---|---|
| < 2 hours | usable fallback |
| 2-24 hours | usable with warning |
| > 24 hours | dashboard warning; do not use for alerts by default |

## Alert Safety on Cache

Default:

```text
alerts_from_cache = false
```

Exception:

User can enable cache alerts later, but V1 should not silently alert from stale source data.

## Parser Failure Handling

If parser fails after a successful source fetch:

- keep raw payload in diagnostics path if debug mode enabled;
- show parse error message;
- fallback to cache if cache is valid;
- do not crash or remove all UI instantly.

## Empty Day Handling

There is a difference between:

```text
source OK + parsed 0 events
```

and:

```text
source failed + 0 events
```

The dashboard must show the distinction.

## Retry Policy

```text
first failure: retry after 60s
second failure: retry after 120s
third+ failure: retry after 300s
manual refresh: immediate
```

## Diagnostics Panel

Minimum status lines:

```text
Source: Live / Cache / Error / Sample
Events: 12 parsed / 8 visible
Last Fetch: 14:23 broker
Next Refresh: 14:24 broker
Broker GMT: Auto +03:00
Parser: OK / error message
```

## Acceptance Gate

Resilience architecture is accepted when:

- missing WebRequest whitelist produces clear diagnostic;
- parser failure does not crash the indicator;
- cache fallback is visibly marked;
- stale cache does not trigger alerts by default;
- empty calendar day is not confused with source failure.
