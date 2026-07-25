# EXP0018 Phase 06 — Host-Timeframe Close Confirmation v2

This package consumes live P05 one-sided transitions, binds each transition to the first eligible host-timeframe candle close, and emits one immutable typed outcome. Existing one-sided states are baselined on fresh attach and are not retroactively confirmed. Pending candidates and finalized observation IDs are checkpointed in MetaTrader Common Files for restart safety. Missed host closes fail closed and require P11 replay.

Run `powershell/run_exp0018_phase06_close_confirmation_v2_checks.ps1`, then compile `EXP0018_Daye_Close_Confirmation_Anatomy.mq5` in MetaEditor.
