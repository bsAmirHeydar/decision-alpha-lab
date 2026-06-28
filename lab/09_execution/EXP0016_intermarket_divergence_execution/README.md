# EXP0016 - Intermarket Divergence Execution

This folder is the execution layer for intermarket divergence strategies.

The detection/research layer can continue to live under `EXP0015_intermarket_time_divergence`, while this folder is reserved for strategies that convert a divergence event into an actionable trade model: entry timing, trade limits, position sizing, stop-loss, take-profit, partial close, daily reset, and audit logs.

## Strategy folders

| Code | Strategy | Status | Source |
| --- | --- | --- | --- |
| EXEC001 | STC SMT Cycles | Documented from source SRS; implementation pending | `STC Expert Advisor SRS.pdf` |

## Folder convention

Each strategy should contain layered documentation before code is written:

1. `README.md` - short navigation and exact status.
2. `01_source_srs_extraction.md` - factual extraction from the provided source.
3. `02_normalized_strategy_spec.md` - normalized English strategy spec.
4. `03_cycle_calendar.md` - time and cycle model.
5. `04_smt_divergence_rules.md` - divergence formation and confirmation rules.
6. `05_execution_and_risk.md` - entries, limits, sizing, SL, TP, partial, resets.
7. `06_mql5_architecture_plan.md` - proposed MQL5 module structure.
8. `07_test_plan.md` - expected scenario tests before live execution.
9. `08_open_questions.md` - contradictions, missing details, and implementation decisions.

## Design principle

Execution logic must stay separated from raw divergence detection. The same SMT/divergence detector should eventually be reusable by Major, Medium, Minor, STC, and any future intermarket timing strategy.
