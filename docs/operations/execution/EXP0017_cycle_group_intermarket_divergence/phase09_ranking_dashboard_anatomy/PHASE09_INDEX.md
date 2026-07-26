# EXP0017 — Phase 09 Ranking Dashboard Anatomy

Phase 09 converts Phase 08 statistical reports into a non-execution ranking and dashboard layer.

It is a research interface only. It does not place orders, filter signals, disable cycle groups, alter risk, change targets, optimize the strategy, or give live trading authority.

## Files

- `PHASE09_RANKING_DASHBOARD_SPEC.md`
- `PHASE09_MQL5_MODULE_ARCHITECTURE.md`
- `PHASE09_SCORE_FORMULA_CONTRACT.md`
- `PHASE09_DASHBOARD_OUTPUT_CONTRACT.md`
- `PHASE09_VALIDATION_AND_TEST_PLAN.md`
- `PHASE09_LIMITS_AND_NON_GOALS.md`
- `PHASE09_HANDOFF_TO_PHASE10.md`
- `PHASE09_OBSIDIAN_GUIDE.md`

## Executable

`mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Ranking_Dashboard_Anatomy.mq5`

## Inputs

Phase 09 reads Phase 08 output CSV files:

- overall report
- by-cycle-group report
- by-direction report
- by-cycle-group-direction report
- by-hunter-clean-role report
- by-cycle-group-direction-role report
- red-flag report

## Outputs

- `EXP0017_Phase09_Rankings_All.csv`
- `EXP0017_Phase09_Rankings_Top.csv`
- `EXP0017_Phase09_Rankings_Bottom.csv`
- `EXP0017_Phase09_Shortlist.csv`
- `EXP0017_Phase09_Dashboard.html`
- `EXP0017_Phase09_Diagnostics.csv`
