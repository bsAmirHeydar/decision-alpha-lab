# Phase 10 — MQL5 Module Architecture

## Expert

`EXP0017_CG_Model_Dataset_Anatomy.mq5`

This expert orchestrates the dataset build. It has no trading functions and performs no chart drawing.

## Include modules

- `CGM_Types.mqh` — config, sample, rank, feature row, summary structs, utilities.
- `CGM_CsvReader.mqh` — reads Phase 07 and Phase 09 CSV files.
- `CGM_FeatureBuilder.mqh` — transforms raw outcome rows into model-ready rows.
- `CGM_Ledger.mqh` — writes dataset, feature dictionary, label summary, diagnostics.
- `CGM_Display.mqh` — compact print/comment summary.
- `CGM_Engine.mqh` — orchestrates read/build/write.

## Data flow

```text
Phase07 Outcome CSV
  -> CGM_CsvReader
  -> SCGMOutcomeSample[]
  -> CGM_FeatureBuilder
  -> SCGMFeatureRow[]
  -> CGM_Ledger
  -> Phase10 dataset outputs
```

Optional enrichment:

```text
Phase09 Rankings/Shortlist
  -> CGM_CsvReader
  -> SCGMRankRow[]
  -> feature row enrichment
```
