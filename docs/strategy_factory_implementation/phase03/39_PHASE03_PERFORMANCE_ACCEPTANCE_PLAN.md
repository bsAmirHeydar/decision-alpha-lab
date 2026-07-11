---
title: "Phase 03 Performance Acceptance Plan"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Metrics

Measure separately:

- terminal tick read latency;
- terminal closed-bar refresh latency;
- cache lookup latency;
- synchronization evaluation latency;
- symbol-spec refresh latency;
- startup warm-up duration;
- memory per registered series.

# Scenarios

1. One symbol, one timeframe.
2. Two symbols, one timeframe.
3. Two symbols, five timeframes.
4. Ten registered series with no changes.
5. History warm-up.
6. Repeated duplicate refreshes.
7. Source failure and recovery.

# Initial targets

These are engineering targets, not guarantees:

```text
cache lookup p99: < 100 microseconds
two-series sync p99: < 200 microseconds
no-change refresh should avoid downstream recalculation
memory remains bounded by declared capacities
```

Terminal `CopyRates` latency is environment-dependent and must be measured separately from in-memory service latency.

# Promotion

Performance failure does not justify bypassing validation or synchronization. Optimize implementation while preserving contracts.
