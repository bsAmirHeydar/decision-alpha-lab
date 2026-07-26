# EXP0017 Phase 08 — Statistical Reports Anatomy

Phase 08 is the first aggregate reporting layer after Phase 07 outcome study.

It reads the Phase 07 outcome-study CSV and produces grouped statistical summaries. It does not trade, rank live signals, filter signals, mutate cycle groups, alter entries, or optimize the strategy.

## Documents

- [[PHASE08_STATISTICAL_REPORTS_SPEC]]
- [[PHASE08_MQL5_MODULE_ARCHITECTURE]]
- [[PHASE08_REPORT_DATA_CONTRACT]]
- [[PHASE08_RED_FLAG_REPORTING_CONTRACT]]
- [[PHASE08_VALIDATION_AND_TEST_PLAN]]
- [[PHASE08_LIMITS_AND_NON_GOALS]]
- [[PHASE08_HANDOFF_TO_PHASE09]]
- [[PHASE08_OBSIDIAN_GUIDE]]

## Code

- `EXP0017_CG_Statistical_Report_Anatomy.mq5`
- `CGS_Types.mqh`
- `CGS_CsvReader.mqh`
- `CGS_Aggregator.mqh`
- `CGS_Ledger.mqh`
- `CGS_Display.mqh`
- `CGS_Engine.mqh`

## Boundary

Phase 08 is a reporting engine, not a decision engine.
