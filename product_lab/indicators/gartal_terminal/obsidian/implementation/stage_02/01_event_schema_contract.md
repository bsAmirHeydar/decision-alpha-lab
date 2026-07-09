---
title: Stage 02 — Event Schema Contract
type: architecture-note
stage: 02
---

# Event Schema Contract

`GT_NewsEvent` is the canonical unit of the product. All future Forex Factory parsing, dashboard rendering, timeline drawing, filtering, alerting, cache writing, and licensing telemetry must route through this structure.

## Required fields

```text
id
sequence
time_source
time_utc
time_broker
day_start_broker
minute_of_day
day_offset
sort_rank
impact_rank
kind
currency
impact
title
normalized_title
actual
forecast
previous
flags
status
source
raw_hash
notes
```

## Design rules

- `time_broker` is the rendering time used on the MT5 chart.
- `time_utc` is retained so the source/parser can be audited later.
- `time_source` preserves the original source interpretation.
- `currency` is always uppercase and trimmed.
- `normalized_title` is lowercase and whitespace-normalized.
- `impact_rank` is numeric so same-minute events can be ordered by severity.
- `kind` separates economic, speech, holiday, breaking, and other events.
- `raw_hash` is not a cryptographic hash; it is a deterministic audit key for duplicate detection and cache comparison.

## Why this matters

The indicator must become a sellable product. Sellable products fail when every UI component invents its own interpretation of a news row. Stage 02 prevents that by making the event object the only language used between modules.
