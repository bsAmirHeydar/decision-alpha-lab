# EXP0016 Intermarket Divergence Execution Documentation

This documentation index points to the execution documentation inside the lab folder.

Main strategy:

- `lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/`

EXEC001 STC SMT Cycles is documented as a layered executable specification and implemented level by level.

Current code level: **Level 14 — Paper Live Alerts**.

Level 14 monitors the full paper/audit pipeline and emits no-order alerts for new signal, paper entry, outcome, partial, and hard-close rows. It still sends no real broker orders.

Key detailed documents:

- `17_implementation_plan.md`
- `18_module_breakdown.md`
- `19_patch_build_sequence.md`
- `21_first_patch_scope.md`
- `22_level_01_skeleton.md`
- `23_level_02_time_engine.md`
- `24_level_03_check_candle_aggregator.md`
- `25_level_04_w_level_builder.md`
- `26_level_05_reference_matrix_hunt_detector.md`
- `27_level_06_smt_candidate_engine.md`

The next engineering stage is Level 07: confirmation, signal registry, and no-late-entry consumption logic.

- [Level 07 STC SMT Confirmation and Signal Registry](LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY.md)
- [Level 13 STC SMT Visualization](LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md)
- [Level 14 STC SMT Paper Live Alerts](LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS.md)


## Level 22 — Hidden Offline License Fix

```text
docs/operations/execution/EXP0016_intermarket_divergence_execution/LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX.md
```

This keeps the STC SMT license behind neutral `InpCycle...` inputs while fixing account-any/server-any validation and improving diagnostics.
