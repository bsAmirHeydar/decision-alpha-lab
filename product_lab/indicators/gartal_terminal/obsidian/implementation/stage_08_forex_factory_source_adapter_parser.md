# Stage 08 — Forex Factory Source Adapter + Parser

## Objective

Stage 08 moves `gartal terminal` from a sample-only news terminal into a live-source-ready macro calendar product.

The primary implementation path is not raw website scraping. The production-safe path is:

```text
Forex Factory / Fair Economy weekly XML feed
        ↓
Downloader EA bridge or local raw file
        ↓
gartal terminal indicator reads local bridge file
        ↓
FF XML parser
        ↓
canonical GT_NewsStore
        ↓
filters / timeline / dashboard / alerts
```

## Critical MT5 Constraint

`GartalTerminal.mq5` is a custom indicator. MT5 custom indicators should not own blocking network calls. The Stage 08 architecture therefore treats direct indicator `WebRequest()` as an unsafe diagnostic path only.

Default live-source architecture:

1. `GartalNewsDownloaderEA.mq5` performs the network request.
2. The EA writes `MQL5/Files/GartalTerminal/ff_calendar_thisweek.xml`.
3. The indicator reads that file via `InpLocalRawFile`.
4. The parser converts XML events into canonical news events.

This keeps the chart UI responsive and avoids binding a commercial indicator to a fragile network call inside the indicator runtime.

## New Inputs

```text
InpForexFactoryUrl
InpSourceFetchMode
InpSourceFormat
InpAllowIndicatorWebRequest
InpLocalRawFile
InpLocalCacheFile
InpSaveRawAfterFetch
InpFallbackToSampleOnSourceFail
InpParserDetectBreakingTitles
InpParserIncludeAllDay
InpParserLogSkippedRows
InpSourceUserAgent
```

## Source Fetch Modes

| Mode | Value | Meaning |
|---|---:|---|
| Local File Bridge | 0 | Indicator reads a raw XML file from `MQL5/Files` |
| WebRequest Attempt | 1 | Diagnostic only; expected to fail in indicators unless runtime permits it |
| Auto | 2 | Try local file first, then unsafe WebRequest only when explicitly allowed |

## Source Formats

| Format | Value | Status |
|---|---:|---|
| Auto | 0 | Detect by content |
| FF XML | 1 | Primary Stage 08 production parser |
| CSV | 2 | Guardrail placeholder |
| Website HTML | 3 | Guardrail placeholder; not production path |

## Why XML over website HTML?

The website calendar DOM is optimized for humans and can change without notice. The XML feed is simpler, smaller, and closer to the historical MT news-indicator workflow.

The parser still keeps `GT_SOURCE_FORMAT_HTML` as a guardrail so accidental website HTML does not silently produce wrong events.

## Event Mapping

Forex Factory XML fields map into `GT_NewsEvent` as follows:

| XML field | Internal field |
|---|---|
| `title` | `event.title` |
| `country` | `event.currency` after country-to-currency mapping |
| `date` + `time` | `event.time_source`, then `event.time_broker` |
| `impact` | `event.impact` |
| `actual` | `event.actual` |
| `forecast` | `event.forecast` |
| `previous` | `event.previous` |
| `url` | `event.notes` |

## Country Mapping

```text
US -> USD
EU/EZ -> EUR
UK/GB -> GBP
JP -> JPY
CH -> CHF
CA -> CAD
AU -> AUD
NZ -> NZD
CN -> CNY
```

## Time Contract

Stage 08 does not guess the source timezone aggressively. It respects the Stage 03 settings:

```text
source time -> UTC -> broker time -> chart objects / dashboard / alerts
```

The user can configure:

```text
InpSourceTimeMode
InpSourceGMTOffsetHours
InpSourceGMTOffsetMinutes
InpBrokerGMTMode
InpBrokerGMTOffsetHours
InpBrokerGMTOffsetMinutes
```

## Breaking News Proxy

True unscheduled breaking-news ingestion requires a separate real-time news source. Stage 08 adds a parser-level proxy:

```text
Trump
President speaks
Emergency
Unscheduled
President statement
```

When these tokens are detected, the event is marked as `is_breaking=true`, which makes it eligible for red/breaking filters and alert logic.

This is not yet a full live headline feed. It is a scheduled-calendar compatible proxy.

## Output Contract

A successful Stage 08 parse must produce:

```text
store.count > 0
store.source_status = FF_XML
runtime.parser_events_added > 0
runtime.parser_last_summary populated
runtime.source_raw_bytes > 0
```

## Failure Contract

If source load or parse fails:

1. Try cache if enabled.
2. If cache fails and fallback is enabled, load sample events.
3. Render dashboard warning diagnostics.
4. Never freeze chart rendering.

## Handoff to Stage 09

Stage 09 will harden:

- cache expiry
- stale-source banners
- source rate-limit control
- parse drift detection
- versioned raw snapshots
- recovery modes
- customer-facing setup diagnostics
