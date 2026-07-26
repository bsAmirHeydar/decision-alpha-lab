# EXP0017 Phase 07 — Signal Outcome Study Anatomy

Phase 07 is the first outcome-study layer after the robot can see time, references, hunts, divergence, confirmation, visual lines, historical backfill, and reference-frontier integrity.

This phase does **not** trade. It does not place orders. It does not change the strategy. It measures what happened after each confirmed tradeable divergence.

## Added MQL5 artifacts

- `EXP0017_CG_Outcome_Study_Anatomy.mq5`
- `CGO_Types.mqh`
- `CGO_OutcomeField.mqh`
- `CGO_Ledger.mqh`
- `CGO_Display.mqh`
- `CGO_Engine.mqh`

## Main output

`EXP0017_Phase07_Outcome_Study.csv`

The CSV is the first model-ready outcome ledger. It links confirmed signal identity to forward outcome windows, MFE, MAE, stop behavior, R result, pip/point result, and daily-range-normalized performance.
