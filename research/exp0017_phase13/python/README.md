# EXP0017 Phase 13 Python Engine

Run only after Phase 12.5 reports `READY_FOR_PHASE13` or an explicitly accepted `READY_WITH_WARNINGS` state.

```powershell
python .\research\exp0017_phase13\python\phase13_controlled_model_comparison.py `
  --data-dir . `
  --out-dir .\research\exp0017_phase13\outputs
```

The engine uses only the Python standard library. It compares deterministic bucket, threshold, logistic, ridge, and constrained-ensemble candidates on the fixed Phase 11 walk-forward folds.

Phase 13 is research-only. No output has execution authority.
