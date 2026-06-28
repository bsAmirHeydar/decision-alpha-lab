# EXP0016 - Intermarket Divergence Execution

This execution area is reserved for strategy implementations built on intermarket divergence logic.

## Current strategy folders

- `EXEC001_STC_SMT_Cycles` - STC Expert Advisor SRS converted into an executable English specification, with owner clarifications.

## Current status

EXEC001 is in documentation/specification phase. The next step is to implement a research/paper engine only after the remaining implementation questions are closed.


## EXEC001 clarification pass 2

The EXEC001 STC SMT Cycles strategy now has a second locked owner decision pass covering touch equality, check-candle anchoring, final-M-candle no-entry, largest-stop reference selection, Entry OFF behavior, offline entry behavior, order failure, M-scoped hedging, volume handling, magic-number ownership, instance locking, restart persistence, and ambiguous SL/TP reporting.
