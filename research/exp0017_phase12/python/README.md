# EXP0017 Phase 12 — Python Research Workbench

This folder contains a research-only Python script for EXP0017.

It reads:

- `EXP0017_Phase10_Model_Dataset.csv`
- `EXP0017_Phase11_Predictions.csv`
- `EXP0017_Phase11_Fold_Metrics.csv`
- `EXP0017_Phase11_Bucket_Validation.csv`

It writes:

- `phase12_data_audit.csv`
- `phase12_oos_leaderboard.csv`
- `phase12_bucket_stability.csv`
- `phase12_feature_drift.csv`
- `phase12_fold_health.csv`
- `phase12_html_report.html`
- `phase12_research_summary.md`

Run from repository root:

```powershell
python .\research\exp0017_phase12\python\phase12_research_workbench.py --data-dir . --out-dir .\research\exp0017_phase12\outputs
```

Boundary: no broker access, no trading, no execution, no strategy mutation.
