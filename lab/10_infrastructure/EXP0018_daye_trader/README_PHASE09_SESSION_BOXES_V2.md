# EXP0018 Phase 09 — Session Boxes v2

Phase 09 renders A/L/N/P rectangles from P03 symbol-local session snapshots. It does not rescan chart bars for range truth and does not consume or create signals.

Run:

```powershell
.\lab\10_infrastructure\EXP0018_daye_trader\powershell\run_exp0018_phase09_session_boxes_v2_checks.ps1 -RepoRoot "."
```

Compile `mql5/Experts/DayeTrader/EXP0018_Daye_Session_Boxes_Anatomy.mq5` with zero errors and zero warnings, then inspect both configured symbol charts.
