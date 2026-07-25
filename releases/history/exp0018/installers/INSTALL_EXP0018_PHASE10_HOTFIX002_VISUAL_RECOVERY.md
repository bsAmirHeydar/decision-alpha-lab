# Install EXP0018 Phase 10 Hotfix002

This patch fixes `INIT_FAILED` and missing P10 drawings caused by broker-specific symbol names and the previous hard dependency on the paired divergence pipeline.

## Compile target

`mql5/Experts/DayeTrader/EXP0018_Daye_Visual_Anatomy.mq5`

## Expected runtime

- On `#USNDAQ100`, the resolver should identify the chart as the NDX-side broker symbol.
- If the SPX counterpart resolves, divergence and temporal layers can both run.
- If the counterpart does not resolve, the Expert still initializes and renders local Daily/Session/Subcycle/Micro/GAP/TDO/TWO anatomy.
- Exact reasons are printed in Experts/Journal.

## Verification

Run:

```powershell
.\lab\10_infrastructure\EXP0018_daye_trader\powershell\run_exp0018_phase10_hotfix002_visual_recovery_checks.ps1 -RepoRoot "."
```

Then compile the Expert in MetaEditor and require `0 errors, 0 warnings`.
