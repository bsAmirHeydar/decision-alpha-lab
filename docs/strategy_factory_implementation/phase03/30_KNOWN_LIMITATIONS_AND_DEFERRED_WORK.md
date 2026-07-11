---
title: "Known Limitations and Deferred Work"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Pending local evidence

The build environment cannot execute MetaEditor. Static checks and Python tests pass, but MQL5 compilation remains a local gate.

# Historical broker offsets

The current terminal source uses configured or inferred current offset. Historical interval-based broker offset calendars are deferred.

# Holidays and early closes

Session primitives support weekdays and times, not exchange holidays or special closes.

# Synthetic timeframes

The terminal source supports standard MetaTrader periods. Arbitrary resampling is deferred.

# Tick history

The Phase 03 cache stores latest ticks only. Historical tick replay belongs to the outcome/replay architecture.

# Gap recovery

Gaps are detected and persist. Automated trusted-source rebuild and recovery audit are deferred.

# Canonical instruments

Exact terminal symbols are preserved. Cross-broker canonical instrument mapping is deferred.

# Multi-account sharing

Each host owns its own market-service bundle in V1. Shared cross-process market services are explicitly out of scope.

# Legacy integration

No existing anatomy has been migrated. This is intentional and will begin only after the plugin SDK and fixture plugin are accepted.
