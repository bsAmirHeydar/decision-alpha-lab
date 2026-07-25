# EXP0018 Phase 01 — New York Time Kernel v2

Run:

```powershell
.\contexts\legacy\infrastructure\exp0018_daye_trader\powershell\run_exp0018_phase01_time_kernel_v2_checks.ps1 -RepoRoot "."
```

The Python validator is an independent reference implementation for the MQL5 time contract. It verifies DST transitions, the 18:00 trading-day rollover, the 17:00–18:00 gap, all A/L/N/P boundaries, all a1–p4 boundaries, and the repeated fall-back hour.
