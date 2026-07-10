# EXP0017 Phase 12.5 Python Integrity Auditor

Run from the repository root after Phase 07 through Phase 11 have produced CSV outputs:

```powershell
python .\research\exp0017_phase12_5\python\phase12_5_pipeline_integrity.py `
  --data-dir . `
  --out-dir .\research\exp0017_phase12_5\outputs
```

Exit codes:

- `0`: ready, or ready with warnings when `--fail-on-warning` is not used.
- `1`: warnings exist and `--fail-on-warning` was requested.
- `2`: a critical readiness gate blocks Phase 13.

The auditor uses only the Python standard library. It has no broker or execution connectivity.
