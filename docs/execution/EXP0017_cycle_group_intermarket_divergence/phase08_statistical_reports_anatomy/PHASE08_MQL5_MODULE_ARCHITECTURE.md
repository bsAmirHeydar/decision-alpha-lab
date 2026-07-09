# Phase 08 — MQL5 Module Architecture

## Expert

```text
EXP0017_CG_Statistical_Report_Anatomy.mq5
```

The expert is a standalone report runner.

## Includes

```text
CGS_Types.mqh
CGS_CsvReader.mqh
CGS_Aggregator.mqh
CGS_Ledger.mqh
CGS_Display.mqh
CGS_Engine.mqh
```

## Module Roles

### `CGS_Types.mqh`

Defines report configuration, outcome sample structure, group statistics, and helper functions.

### `CGS_CsvReader.mqh`

Reads the Phase 07 CSV and maps rows into `SCGSOutcomeSample` records.

### `CGS_Aggregator.mqh`

Groups samples by selected dimensions and computes statistics.

### `CGS_Ledger.mqh`

Writes report CSV files.

### `CGS_Display.mqh`

Builds compact chart/Experts summaries.

### `CGS_Engine.mqh`

Coordinates the full report run.

## Design Principle

The statistical report engine is intentionally separate from execution logic. It reads data already produced by Phase 07 and writes reports. It does not observe live ticks for trade decisions.
