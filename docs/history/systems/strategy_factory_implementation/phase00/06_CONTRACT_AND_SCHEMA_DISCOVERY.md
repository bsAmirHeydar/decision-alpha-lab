---
title: "Contract and Schema Discovery"
tags: [strategy-factory, phase-00, contracts, schema]
status: canonical
---

# Contract and Schema Discovery

## Purpose

Phase 01 will freeze explicit canonical contracts. Phase 00 therefore maps the implicit contracts already relied upon by current code.

## Discovered public classes

### `MT5Connector`

Public behavior:

- `connect()`
- `disconnect()`
- `fetch(...)`

Implicit assumptions:

- `MetaTrader5` is importable at module-import time;
- terminal initialization is global;
- symbol validation uses current terminal symbols;
- returned time values are terminal-local/naive;
- DataFrame columns are fixed by the connector;
- full-history retrieval is chunked by position.

### `MarketDataEngine`

Public behavior:

- `fetch(...)`
- `get_df(...)`
- `iOpen`, `iClose`, `iHigh`, `iLow`, `iTime`, `iVolume`, `iSpread`

Implicit assumptions:

- data is pandas-based;
- `time` uniquely identifies a bar;
- latest bar may be forming and is re-fetched;
- cache location is globally fixed;
- candle access uses MQL-style shifts.

### `ParquetStore`

Public behavior:

- `save`
- `load`
- `delete`
- `exists`

Missing contract dimensions:

- schema version;
- source hash;
- producer version;
- atomicity;
- file locking;
- corruption detection;
- run identity;
- partition policy;
- retention policy.

### `LRuleNodeDetector`

Public behavior:

- `detect`
- `iNode`
- `iHighNode`
- `iLowNode`

This is an anatomy contract, not a kernel contract. The public output currently uses DataFrame rows and implicit columns.

### `M0001RTV`

Public behavior:

- `compute`

The implementation constructor requires an `engine` and `detector`. The legacy test passes `L` instead of `detector`, demonstrating contract drift. Phase 01 must freeze the dependency interface before any migration.

## Contract debt

None of the current contracts contain:

- schema major/minor version;
- stable event identity;
- source lineage;
- known-time semantics;
- creation time;
- producer version;
- explicit missing-value behavior;
- serialization compatibility.

## Phase 01 input

The machine-readable contract map is:

```text
lab/11_strategy_factory/phase00_current_state_audit/artifacts/contract_schema_map.csv
```

Phase 01 must not blindly preserve every public method. It must decide which are compatibility shims, which are canonical, and which are strategy-specific.
