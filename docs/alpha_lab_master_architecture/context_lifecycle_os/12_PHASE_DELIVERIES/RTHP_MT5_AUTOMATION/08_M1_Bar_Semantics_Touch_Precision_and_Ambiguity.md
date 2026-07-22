---
title: RTHP MT5 Automation — M1 Bar Semantics, Touch Precision, and Ambiguity
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, m1, touch, known-time, ambiguity]
---

# M1 Bar Semantics, Touch Precision, and Ambiguity

## Canonical M1 record

Each closed bar must contain:

```text
canonical_instrument_id
broker_symbol
timeframe_seconds = 60
bar_open_time_utc_ms
bar_close_time_utc_ms
known_time_utc_ms
open
high
low
close
tick_volume
spread
real_volume
source_sequence
source_terminal_id
source_revision
```

## Causal availability

- `bar_open_time_utc_ms` is the interval start.
- `bar_close_time_utc_ms` is the first instant after the represented interval.
- `known_time_utc_ms` is at least the bar close and is the causal availability cut used by replay.
- `ingested_at_utc_ms` is provenance only and must not replace historical known time.

## Touch rules from M1 OHLC

For a symbol-local reference level:

```text
High touch: bar.high >= reference_high
Low touch:  bar.low  <= reference_low
```

The exact tick timestamp is unknown. Store:

```text
touch_time_resolution = M1_INTERVAL
touch_interval_start = bar_open_time
touch_interval_end = bar_close_time
first_observable_touch_time = bar_close_time
```

## No intrabar-order inference

The system must not infer whether Open, High, Low, or Close occurred first. It must not synthesize an OHLC path or pseudo-ticks.

If both corresponding symbol levels are touched inside the same M1 interval, the state after that interval is `BOTH_SIDES_TOUCHED`; no exclusive first-touch ordering is claimed.

If a single symbol touches both its High-side and Low-side references in one M1 bar, both side observations may be recorded independently, but their order remains unknown.

## M15 confirmation

RTHP relationship confirmation uses only fully closed M1 bars within the synchronized M15 interval. Missing synchronized data preserves `UNCONFIRMED`; stale data cannot confirm.
