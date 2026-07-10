# Phase 12.5 MQL5 Module Architecture

## Expert

`EXP0017_CG_Pipeline_Integrity_Anatomy.mq5`

The Expert is an offline orchestration shell. `OnTick()` intentionally does nothing.

## Modules

### `CGPI_Types.mqh`

Defines configuration, severity, relation modes, file contracts, audit rows, schema issues, reconciliation rows, metric checks, readiness gates, and summary statistics.

### `CGPI_Contracts.mqh`

Owns canonical schemas for Phase 07–11 files. Centralizing contracts prevents every reader from inventing its own interpretation.

### `CGPI_CsvInspector.mqh`

Provides:

- quoted CSV parsing;
- header inspection;
- required-column validation;
- primary-key extraction;
- duplicate and empty-key detection;
- timestamp parse/order checks;
- metric/value reading;
- conditional row counting.

### `CGPI_Reconciler.mqh`

Builds exact and child-subset lineage checks, writer metric reconciliations, and readiness gates.

### `CGPI_Ledger.mqh`

Writes evidence files. It never writes to upstream research artifacts.

### `CGPI_Display.mqh`

Emits a compact Experts-tab summary. Chart comments are disabled by default.

### `CGPI_Engine.mqh`

Runs contracts → inspection → reconciliation → metrics → gates → outputs.

## Output files

- `EXP0017_Phase12_5_File_Audit.csv`
- `EXP0017_Phase12_5_Schema_Issues.csv`
- `EXP0017_Phase12_5_Key_Reconciliation.csv`
- `EXP0017_Phase12_5_Metric_Reconciliation.csv`
- `EXP0017_Phase12_5_Readiness_Gates.csv`
- `EXP0017_Phase12_5_Readiness_Summary.csv`
- `EXP0017_Phase12_5_Diagnostics.csv`

## Performance boundary

MQL5 audits are bounded by configurable row/key caps. The Python auditor is the authoritative deep row-level audit for large datasets.
