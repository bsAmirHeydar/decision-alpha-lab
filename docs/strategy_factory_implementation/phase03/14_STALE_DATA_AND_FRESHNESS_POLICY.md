---
title: "Stale Data and Freshness Policy"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Freshness is contextual

A five-second-old tick may be acceptable for one market and invalid for another. A one-minute bar may remain valid for a slow feature but not for a cycle-bound decision.

Phase 03 therefore stores timestamps and exposes configurable thresholds rather than embedding one global definition.

## Tick freshness

The tick cache uses receive time and `max_age_milliseconds`. Retrieval fails when the threshold is exceeded.

## Bar freshness

Multi-symbol requirements use latest close time and per-series maximum staleness.

## Later feature freshness

Phase 07 will add feature TTLs and dependency generations. That layer will consume Phase 03 source generations and timestamps.

## Fail-closed path

If required data is stale:

```text
no snapshot
→ no candidate
→ no model call
→ no execution intent
```

An abstention is a valid system output and must be visible in telemetry.

## Clock skew

If source or receive timestamps appear in the future, the state is invalid rather than merely stale. This distinction supports incident diagnosis.
