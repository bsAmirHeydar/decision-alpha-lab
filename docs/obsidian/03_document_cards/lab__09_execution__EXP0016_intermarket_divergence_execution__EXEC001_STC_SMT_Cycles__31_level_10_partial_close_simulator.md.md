---
title: "Level 10 — Paper Partial Close Simulator and W4 Management"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/level_10_paper_partial_close_simulator_w4_management/91dce4903990_31_level_10_partial_close_simulator.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "3233"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# Level 10 — Paper Partial Close Simulator and W4 Management

**Source:** [[docs/evidence/level_10_paper_partial_close_simulator_w4_management/91dce4903990_31_level_10_partial_close_simulator|docs/evidence/level_10_paper_partial_close_simulator_w4_management/91dce4903990_31_level_10_partial_close_simulator.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `3233` bytes

## خلاصه

Level 10 adds the first paper position-management layer after the Level 09 paper outcome simulator. It does not place real orders, does not modify broker positions, and does not perform hard-close accounting yet. Its only new responsibility is to decide what would happen at the end of W4 for open paper trades. The locked STC rule is: If Partial is OFF, no partial action is taken. If Partial is ON, at the end of W4 of the same M, every trade opened in that M is checked. If the trade has already reached TP, SL, or an ambiguous SL/TP state before or at the W4 checkpoint, no partial action is taken. If the trade is still open at the W4 checkpoint, about 50% of the volume is closed. The 50% close

## Headings

- Level 10 — Paper Partial Close Simulator and W4 Management
-   Scope
-   Inputs added
-   New output
-   Algorithm
-   Examples
-   What is still deferred

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[docs/evidence/04_smt_divergence_rules_algorithms/5dba5ebb5e42_04_smt_divergence_rules|04 - SMT Divergence Rules and Algorithms]] — `experiment`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06 - MQL5 Architecture Plan]] — `experiment`
- [[docs/evidence/07_test_plan/ad357cabb5f5_07_test_plan|07 - Test Plan]] — `experiment`
- [[docs/evidence/08_open_questions/18e20583bb82_08_open_questions|08 - Open Questions]] — `experiment`
- [[docs/evidence/09_owner_decisions_pass_1/d64c20e06d5e_09_owner_decisions_pass_1|09 - Owner Decisions Pass 1]] — `experiment`
- [[docs/evidence/11_algorithm_layers/07355f60fef2_11_algorithm_layers|11 - Algorithm Layers]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines|12 - State Machines]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13 - Data Model and Journals]] — `experiment`
- [[docs/evidence/14_backtest_live_runtime/c31f0574e3ec_14_backtest_live_runtime|14 - Backtest and Live Runtime]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
