# LEVEL 09 — STC SMT Paper Outcome Simulator

This level adds the audit-only paper outcome layer for EXEC001 STC SMT Cycles.

It scans closed check candles after planned paper entries and writes TP, SL, AMBIGUOUS, or OPEN_UNRESOLVED outcomes to:

```text
Common Files/dal/stc/EXEC001_STC_SMT_Cycles/stc_level09_paper_outcomes.csv
```

No live order, partial close, hard close, or drawing is enabled in this level.
