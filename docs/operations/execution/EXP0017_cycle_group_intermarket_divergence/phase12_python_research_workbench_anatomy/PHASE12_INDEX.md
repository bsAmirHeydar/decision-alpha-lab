# EXP0017 Phase 12 — Python Research Workbench & Experiment Registry

Phase 12 creates the external research bridge after walk-forward validation.

It does not trade. It does not mutate the strategy. It does not promote any CG, direction, role, feature, or model into live execution.

## Inputs

- Phase 07 outcome-study CSV
- Phase 08 statistical report CSVs
- Phase 09 ranking/shortlist CSVs
- Phase 10 model dataset CSV
- Phase 11 walk-forward prediction and validation CSVs

## Outputs

MQL5 bridge outputs:

- `EXP0017_Phase12_File_Inventory.csv`
- `EXP0017_Phase12_Research_Manifest.json`
- `EXP0017_Phase12_Experiment_Registry_Template.csv`
- `EXP0017_Phase12_Python_Run_Plan.md`
- `EXP0017_Phase12_Diagnostics.csv`

Python workbench outputs:

- `phase12_data_audit.csv`
- `phase12_oos_leaderboard.csv`
- `phase12_bucket_stability.csv`
- `phase12_feature_drift.csv`
- `phase12_fold_health.csv`
- `phase12_html_report.html`
- `phase12_research_summary.md`

## Boundary

Phase 12 is a research bridge. It is not a decision engine.
