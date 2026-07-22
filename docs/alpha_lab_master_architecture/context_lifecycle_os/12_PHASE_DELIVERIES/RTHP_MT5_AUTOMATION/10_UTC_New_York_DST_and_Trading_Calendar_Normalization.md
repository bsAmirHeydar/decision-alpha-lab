---
title: RTHP MT5 Automation — UTC, New York DST, and Trading Calendar Normalization
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, time, utc, new-york, dst]
---

# UTC, New York DST, and Trading Calendar Normalization

## Source time

MetaTrader bar times are treated as UTC open times. Acquisition requests use timezone-aware UTC datetimes.

## Stored time fields

Every canonical M1 record stores:

- absolute UTC open time;
- absolute UTC close time;
- causal known time;
- derived `America/New_York` local time;
- UTC offset;
- DST fold where relevant;
- New York trading-day identity;
- session and cycle membership.

## Cycle construction

All RTHP intervals remain half-open and are derived using the versioned New York calendar and cycle registry. The adapter does not use broker-server local time to define RTHP cycles.

## DST rules

- Spring-forward missing local hour is represented by absolute UTC continuity and local-calendar semantics.
- Fall-back repeated local hour remains distinguishable by absolute time and fold.
- No local timestamp without offset/fold is accepted as a canonical identity.

## Calendar classification

Each expected M1 interval is classified as:

```text
JOINTLY_OPEN
PRIMARY_ONLY_OPEN
SECONDARY_ONLY_OPEN
MARKET_CLOSED
HOLIDAY_OR_EARLY_CLOSE
UNKNOWN_CALENDAR_STATE
```

Unknown calendar states block canonical acceptance.
