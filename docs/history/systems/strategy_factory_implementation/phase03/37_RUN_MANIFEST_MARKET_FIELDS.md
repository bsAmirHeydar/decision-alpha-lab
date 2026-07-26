---
title: "Run Manifest Market Fields"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Required market lineage

Every research, tester, paper, or live run should eventually record:

```yaml
market_source_id:
terminal_build:
broker_server:
account_mode:
broker_utc_mapping_version:
broker_utc_offset_minutes:
time_kernel_version:
session_schedule_version:
symbol_universe:
timeframes:
bar_cache_capacity:
missing_bar_policy:
tick_freshness_ms:
sync_requirements:
symbol_spec_generations:
```

# Why

Two apparently identical strategies can produce different events because of feed, timezone, symbol contract, or gap policy. Without market lineage, results cannot be compared or reproduced.

# Hashing

The compiled run manifest should have a stable hash that is attached to events, snapshots, models, and execution traces. A change in market semantics creates a new run generation.

# Phase ownership

Phase 05 will implement full artifact identity and manifest compilation. Phase 03 defines the market fields that must be included.
