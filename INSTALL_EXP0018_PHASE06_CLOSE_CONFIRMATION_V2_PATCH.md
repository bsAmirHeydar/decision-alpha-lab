# Install EXP0018 Phase 06 — Host-Timeframe Close Confirmation v2

1. Extract this ZIP at the Decision Alpha Lab repository root.
2. Run `lab/10_infrastructure/EXP0018_daye_trader/powershell/run_exp0018_phase06_close_confirmation_v2_checks.ps1`.
3. Compile `mql5/Experts/DayeTrader/EXP0018_Daye_Close_Confirmation_Anatomy.mq5` in MetaEditor.
4. Require `0 errors, 0 warnings` and embedded P05/P06 self-test PASS.
5. Attach the Expert before the intended live transition window; fresh attach baselines existing one-sided states without retroactive confirmation.
6. Keep checkpoint persistence enabled for restart-before-close safety.
7. Inspect Experts/Journal and optional Common Files audit CSV.

Rollback: remove the files listed in the manifest. Preserve audit files before deleting the namespaced Common Files checkpoint.
