---
title: RTHP MT5 Automation — M1 Canonical Data Floor and Sub-M1 Exclusion
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, m1, data-quality]
---

# M1 Canonical Data Floor and Sub-M1 Exclusion

## Doctrine

The production research path uses **closed one-minute bars as its lowest canonical market-data resolution**.

## Rationale

Sub-M1 broker history can be inconsistent across terminals, brokers, symbols, sessions, and retention windows. It also increases microstructure noise, feed-specific artifacts, timestamp irregularity, and false precision. The RTHP context is confirmed on synchronized M15 cuts and does not require a fabricated tick-level path.

## Hard rules

```text
canonical_source_timeframe = M1
sub_m1_source_allowed = false
raw_tick_history_required = false
higher_timeframes_derived_from_m1 = true
current_incomplete_m1_bar_allowed = false
synthetic_ticks_from_ohlc_allowed = false
```

## Consequences

- Historical acquisition requests M1 bars, not tick history.
- M5, M15, H1, Daily, Weekly, and custom cycles are aggregated from M1.
- The final incomplete M1 bar is dropped.
- Intrabar order is represented as unknown.
- Any future sub-M1 experiment must use a separate non-canonical profile and may not silently mix with M1 research results.
