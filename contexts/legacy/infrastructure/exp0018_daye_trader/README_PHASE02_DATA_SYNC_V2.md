
# EXP0018 Phase 02 — Multi-Symbol Data Synchronization v2

This package validates the exact-timestamp, no-forward-fill data boundary used by downstream EXP0018 period, hunt, and replay phases.

Run:

```powershell
.\contexts\legacy\infrastructure\exp0018_daye_trader\powershell\run_exp0018_phase02_data_sync_v2_checks.ps1 -RepoRoot "."
```

The validator does not replace MetaEditor compilation or terminal runtime review.
