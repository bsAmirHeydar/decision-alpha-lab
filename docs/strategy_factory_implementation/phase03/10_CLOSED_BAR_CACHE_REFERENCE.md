---
title: "Closed Bar Cache Reference"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Purpose

The closed-bar cache is the canonical in-memory history for shared strategy consumption. Only closed bars enter the Phase 03 terminal source.

## Series key

```text
terminal symbol + timeframe seconds
```

Each series owns:

- a bounded ordered array;
- capacity;
- persistent gap flag;
- generation counter.

## Upsert semantics

- older open time: reject;
- identical open time and identical content: duplicate;
- identical open time with changed content: replace and increment generation;
- next expected open time: insert;
- later-than-expected open time: insert and mark gap.

## Gap persistence

Once a gap is detected, the series remains gapped until a future recovery/rebuild operation explicitly reconstructs continuity. Silent healing would conceal data-quality incidents from downstream features.

## Capacity

Oldest bars are removed when capacity is reached. Capacity is a runtime resource decision and must be large enough for the maximum lookback declared by active plugins. Phase 04 capability descriptors will declare those requirements before a plugin can start.

## Closed-bar invariant

The terminal source calls `CopyRates` with start position 1. Current forming bars are excluded from canonical history. Tick-sensitive features may use the tick cache separately, but they must declare that dependency.
