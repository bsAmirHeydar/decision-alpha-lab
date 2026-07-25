# INSTALL — EXP0017 Phase 12.5 Pipeline Integrity Patch

## Scope

Adds the mandatory pipeline-integrity barrier before Phase 13 controlled model comparison.

## Main entry points

- MQL5: `mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Pipeline_Integrity_Anatomy.mq5`
- Python: `research/exp0017_phase12_5/python/phase12_5_pipeline_integrity.py`
- PowerShell: `research/exp0017_phase12_5/powershell/run_phase12_5_integrity.ps1`

## Execution order

1. Generate Phase 07 through Phase 11 CSV outputs.
2. Compile and run the Phase 12.5 MQL5 Expert for Terminal-side preflight.
3. Copy or point Python to the directory containing those CSV files.
4. Run the PowerShell/Python deep audit.
5. Review readiness gates before starting Phase 13.

## Boundary

No trading, order management, filtering, risk mutation, target mutation, or model promotion is added.
