# Phase 09 MQL5 Module Architecture

## Expert

`EXP0017_CG_Ranking_Dashboard_Anatomy.mq5`

The expert is standalone and report-only. It runs on init or timer, reads CSV reports, writes ranking outputs, and optionally shows a compact comment dashboard.

## Include Modules

| Module | Responsibility |
|---|---|
| `CGRK_Types.mqh` | Ranking structs, config, enums, helpers |
| `CGRK_CsvReader.mqh` | Reads Phase 08 CSV report rows |
| `CGRK_Ranker.mqh` | Calculates scores, grades, shortlist flags |
| `CGRK_Ledger.mqh` | Writes CSV and HTML dashboard outputs |
| `CGRK_Display.mqh` | Optional chart comment summary |
| `CGRK_Engine.mqh` | Orchestrates loading, scoring, sorting, writing |

## Dependency Direction

Phase 09 does not rebuild market anatomy. It only consumes Phase 08 files. The dependency chain is:

```text
Phase 07 Outcome Study CSV
  -> Phase 08 Statistical Reports
    -> Phase 09 Ranking Dashboard
```

## Why Phase 09 Avoids Signal Logic

If Phase 09 recalculated signals, it would risk doctrine drift. It could accidentally use different time, reference, frontier, hunt, confirmation, or outcome logic. Therefore it reads report outputs only.
