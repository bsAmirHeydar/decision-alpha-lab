---
title: "Market Health and Telemetry"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Counters

Phase 03 records:

- tick updates, hits, and misses;
- bar refreshes, insertions, replacements, duplicates;
- detected gaps;
- synchronization checks and failures;
- specification refreshes;
- source errors;
- last and maximum refresh latency.

## Purpose

Telemetry answers whether the platform is healthy before strategy performance is considered. A profitable backtest produced by frequent data gaps is not acceptable evidence.

## Future SLOs

Later monitoring will derive:

- cache-hit ratio;
- stale-data rate;
- synchronization success rate;
- source-error rate;
- p50/p95/p99 refresh latency;
- specification drift count.

## Cardinality

Telemetry counters remain low-cardinality and in memory on the fast path. Detailed per-event diagnostics belong in the audit ledger, not in metric labels.

## Alerts

Phase 19 will connect health states to abstention, model disablement, and operational alerts. Phase 03 provides the raw state and counters.
