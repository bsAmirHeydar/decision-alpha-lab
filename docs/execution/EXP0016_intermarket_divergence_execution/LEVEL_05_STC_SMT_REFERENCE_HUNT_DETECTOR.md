# Level 05 — STC SMT Reference Matrix and Raw Hunt Detector

Level 05 adds the previous-W reference matrix and raw touch-only hunt detector for `EXEC001_STC_SMT_Cycles`.

It is still an audit-only level. It creates no SMT candidate, no confirmation, no signal, no paper trade, and no live order.

## Files

EA:

- `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`

New module:

- `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Hunts.mqh`

Updated modules:

- `DAL_STC_Enums.mqh`
- `DAL_STC_Types.mqh`
- `DAL_STC_Config.mqh`
- `DAL_STC_Utils.mqh`
- `DAL_STC_Journal.mqh`
- `DAL_STC_Engine.mqh`

Strategy documentation:

- `lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector.md`

## Output

Common Files output:

- `dal/stc/EXEC001_STC_SMT_Cycles/stc_level05_build_sanity.csv`
- `dal/stc/EXEC001_STC_SMT_Cycles/stc_level05_runtime_events.csv`
- `dal/stc/EXEC001_STC_SMT_Cycles/stc_level05_time_audit.csv`
- `dal/stc/EXEC001_STC_SMT_Cycles/stc_level05_check_candles.csv`
- `dal/stc/EXEC001_STC_SMT_Cycles/stc_level05_w_levels.csv`
- `dal/stc/EXEC001_STC_SMT_Cycles/stc_level05_reference_hunts.csv`

## Runtime inputs added

- `InpWriteHuntAudit`
- `InpMaxHuntBackfillOnInit`
- `InpMaxHuntCatchupPerPulse`

## Locked behavior

- Equality is touch.
- No tolerance is applied.
- W1 has no reference and no signal.
- W2 references W1 only.
- W3 references W2 and W1.
- W4 references W3, W2, and W1.
- Raw high hunt is checked against each symbol's own reference high.
- Raw low hunt is checked against each symbol's own reference low.
- Both symbols must have complete current check-candle and reference-W data.
- The layer is audit-only.
