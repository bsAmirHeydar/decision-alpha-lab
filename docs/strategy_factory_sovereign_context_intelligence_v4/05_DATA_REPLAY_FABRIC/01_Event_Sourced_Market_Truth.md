---
title: Event-Sourced Market Truth
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Provide a replayable source of market, broker, calendar, and symbol-state events from which all known-time features and outcomes are derived.

## Capability tier

**Core Production**

## System design

### Event model

Ticks, quotes, trades, bars, symbol specifications, sessions, news/calendar state, broker responses, and clock events are immutable records.

### Bitemporal semantics

Event time and knowledge/ingestion time are distinct; corrections create new records rather than rewriting history.

### Replay cursor

Every materialization records exact partitions, offsets, timezone rules, and event-order policy.

### Feed federation

Multiple feeds remain separate evidence domains until an explicit normalization and cross-feed study is performed.

## Input contracts

- `RawEventPartitions`
- `CalendarVersion`
- `SymbolSpecHistory`

## Output contracts

- `ReplayManifest`
- `EventCursor`
- `DataQualityIncidents`

## Measurement framework

- Replay determinism.
- Gap and duplicate rates.
- Clock skew.
- Cross-feed divergence.

## Adversarial questions

- Can later corrections leak into earlier decisions?
- Are bar closes reconstructed with inconsistent session calendars?
- Does feed normalization erase meaningful execution differences?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[Known_Time_And_Bitemporal_Lineage]]
