# Install EXP0018 Phase 07 — Reference Lifecycle v2

1. Extract this ZIP at the Decision Alpha Lab repository root.
2. Run `lab/10_infrastructure/EXP0018_daye_trader/powershell/run_exp0018_phase07_reference_lifecycle_v2_checks.ps1`.
3. Compile `mql5/Experts/DayeTrader/EXP0018_Daye_Reference_Lifecycle_Anatomy.mq5` in MetaEditor.
4. Require `0 errors, 0 warnings` and embedded P06/P07 self-test PASS.
5. Keep both P06 and P07 Common Files checkpoints enabled.
6. Validate one exact opportunity, one accepted use; distinct later opportunity, another accepted use while protected survives.
7. Validate protected touch, double hunt, and role switch retirement.
8. Inspect Experts/Journal and optional Common Files audit CSV.

Rollback: preserve audit/checkpoint files, remove manifest-listed files, and restore the pre-P07 `DAYE_ConfirmationEngine.mqh` if P07 is fully removed.
