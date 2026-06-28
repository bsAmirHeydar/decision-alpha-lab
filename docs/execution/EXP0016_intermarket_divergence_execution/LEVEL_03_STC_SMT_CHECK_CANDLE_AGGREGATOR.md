# LEVEL 03 — STC SMT Check Candle Aggregator

This document mirrors the implementation-level notes for:

`lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/24_level_03_check_candle_aggregator.md`

Level 03 adds the M1-based check-candle data layer for EXEC001 STC SMT Cycles.

It does not add W levels, SMT detection, signal generation, paper trading, drawing, partial close, hard close, or auto trading.

Generated Common Files outputs:

- `dal/stc/EXEC001_STC_SMT_Cycles/stc_level03_build_sanity.csv`
- `dal/stc/EXEC001_STC_SMT_Cycles/stc_level03_runtime_events.csv`
- `dal/stc/EXEC001_STC_SMT_Cycles/stc_level03_time_audit.csv`
- `dal/stc/EXEC001_STC_SMT_Cycles/stc_level03_check_candles.csv`
