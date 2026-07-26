---
title: "File-by-File Decision Ledger"
tags: [strategy-factory, phase-00, migration-ledger]
status: canonical
---

# File-by-File Decision Ledger

This document summarizes the binding disposition of the implemented files in the audited snapshot. The full row-level inventory remains machine-readable in `repository_inventory.csv` and `module_classification.csv`.

## Market-data package

### `connectors/MT5Connector.py`

**Disposition:** Adapt.

Preserve:

- explicit connect/disconnect lifecycle;
- symbol validation;
- range, days, bar-count, and history retrieval modes;
- standardized OHLCV projection.

Change:

- move `MetaTrader5` import behind a vendor adapter boundary;
- return canonical bars rather than an unversioned DataFrame contract;
- require explicit source timezone and UTC conversion;
- replace `datetime.now()` with an injected clock;
- expose retries and terminal errors as typed transport failures;
- separate data-read authority from future broker authority.

### `services/MarketDataEngine.py`

**Disposition:** Wrap, then incrementally migrate.

Preserve:

- incremental refresh behavior;
- re-fetching a potentially forming latest bar;
- MQL-style shift accessors needed by migrated anatomy engines;
- deduplicated chronological storage.

Change:

- inject storage rather than constructing `ParquetStore` internally;
- bind cache identity to source/schema/producer versions;
- make closed/forming-bar status explicit;
- remove naive clock assumptions;
- stop treating DataFrame row order as identity.

### `cache/ParquetStore.py`

**Disposition:** Adapt into future Artifact Store internals.

Preserve:

- simple Parquet persistence;
- deterministic symbol/timeframe partition concept;
- load/delete/exists semantics.

Change:

- atomic temporary-write then rename;
- hash verification;
- schema metadata;
- manifest sidecar;
- concurrency control;
- immutable run artifacts;
- retention policy.

### `utils/timeframes.py`

**Disposition:** Adapt.

The concept is reusable, but the enum currently imports vendor constants. Phase 01/02 should separate canonical timeframe identity from MT5-specific values.

### `exceptions.py`

**Disposition:** Reuse conceptually, migrate package location.

Exceptions remain useful but should inherit from a shared error taxonomy that distinguishes configuration, transport, data-quality, causality, and execution failures.

## Structural-node package

### `detectors/L_Rule.py`

**Disposition:** Wrap.

Preserve exact node semantics until golden replay proves parity. Do not rewrite equality behavior, confirmation horizon, or incremental rebuild during contract work.

Required adapter outputs:

- stable node identity;
- node event time;
- known/confirmation time;
- node type;
- node price;
- confirmed/provisional status;
- source data identity;
- anatomy version.

Persistence methods inside the detector become legacy compatibility behavior after the Artifact Store exists.

### `metrics/M0001_relative_territory_volatility.py`

**Disposition:** Wrap and repair contract drift.

Preserve:

- zone-ratio geometry;
- exit-gap lifecycle;
- touch/hunt consumption modes;
- revisit identity;
- event-level RTV output.

Required changes:

- constructor contract freeze;
- explicit detector dependency;
- canonical input/output records;
- no private cache lifecycle;
- known-time and label-end semantics;
- deterministic fixture coverage.

### Legacy test files

**Disposition:** Migrate.

They remain useful as operator diagnostics but must not be the unit-test gate. Rename or mark them as live integration scripts after deterministic tests exist.

## Research lifecycle folders

### Observation and hypothesis documents

**Disposition:** Reuse.

They preserve research rationale and should be linked to future experiment manifests through stable IDs.

### Experiment directories

**Disposition:** Migrate.

Empty scripts and reports are replaced by generated run folders. Human interpretation remains in Markdown, but dataset, configuration, fold, prediction, and QA artifacts become machine-generated.

### Validation, production, monitoring, archive

**Disposition:** Preserve ownership concepts, replace placeholder content.

These directory names express a valid lifecycle. The Strategy Factory should populate them through promotion state, not manual copying.

## Repository artifacts

### `lab/cache_data`, `lab/cache_nodes`, `lab/cache_metrics`

**Disposition:** Migrate, retain during differential validation.

Never delete before canonical artifacts reproduce the same logical outputs and rollback is tested.

### `__pycache__`, `.pytest_cache`

**Disposition:** Delete later after ignore rules are installed.
