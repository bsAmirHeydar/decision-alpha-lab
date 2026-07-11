---
title: "Duplicate Capability Analysis"
tags: [strategy-factory, phase-00, duplication, architecture]
status: canonical
---

# Duplicate Capability Analysis

Three overlapping capability families were identified.

## 1. Parquet artifact persistence

Implementations:

1. `ParquetStore`
2. node persistence inside `LRuleNodeDetector`
3. metric persistence inside `M0001RTV`

### Why this is duplication

Each implementation performs some combination of:

- path construction;
- directory creation;
- Parquet read/write;
- naming by symbol/timeframe/parameter;
- cache existence checks;
- replacement of old data.

### Risk

Independent conventions create:

- incompatible identities;
- stale-cache ambiguity;
- untracked schema changes;
- partial-write risk;
- inconsistent deletion;
- inability to reproduce a run from metadata.

### Decision

Create one versioned `ArtifactStore` in Phase 05. Domain modules retain serializer/adaptor responsibility but do not own physical storage semantics.

## 2. Market-bar normalization

Implementations:

- `MT5Connector`
- `MarketDataEngine`

Both remove duplicates, sort by time, and reset indexes.

### Decision

Phase 01 defines a canonical bar contract. The vendor connector maps vendor data to the contract. The market-data service validates and persists it. Repeated normalization may remain temporarily for compatibility, but one layer becomes authoritative.

## 3. Manual live test harnesses

Implementations:

- connector test script;
- market-data test script;
- structural-node detector test script;
- M0001 metric test script.

These scripts create live MT5 connections, fetch broker data, print output, and are collected by pytest despite not being deterministic unit tests.

### Decision

Split testing into:

```text
Unit tests
→ no terminal, deterministic fixtures

Contract tests
→ fake connectors and canonical records

Integration tests
→ optional live MT5, explicitly marked

Golden replay tests
→ frozen data and expected anatomy/metric output
```

## General duplicate-resolution rule

When multiple implementations share mechanics but differ in market meaning:

- centralize mechanics;
- preserve market meaning in plugins;
- add differential tests before retiring old paths;
- never merge by deleting the only working implementation first.
