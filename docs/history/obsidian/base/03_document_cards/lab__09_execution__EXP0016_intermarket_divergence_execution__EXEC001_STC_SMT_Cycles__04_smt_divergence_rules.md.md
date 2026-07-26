---
title: "04 - SMT Divergence Rules and Algorithms"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/04_smt_divergence_rules_algorithms/5dba5ebb5e42_04_smt_divergence_rules.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "6564"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# 04 - SMT Divergence Rules and Algorithms

**Source:** [[docs/evidence/04_smt_divergence_rules_algorithms/5dba5ebb5e42_04_smt_divergence_rules|docs/evidence/04_smt_divergence_rules_algorithms/5dba5ebb5e42_04_smt_divergence_rules.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `6564` bytes

## خلاصه

SMT divergence is defined only between Symbol1 and Symbol2. The strategy compares each symbol against its own W-cycle reference levels. It never compares one symbol's absolute price level to the other symbol's absolute price level. Inside each M: W1 has no eligible references and cannot signal. W2 references W1. W3 references W2 and W1. W4 references W3, W2, and W1. The current W never references itself. No W may reference a W from another M. No W may reference a W from a previous STC trading day. For each symbol, each completed W produces: W ID. Symbol. M ID. Start time. End time. High. Low. Data completeness status. The reference levels used by the current W are the completed previous W re

## Headings

- 04 - SMT Divergence Rules and Algorithms
-   1. Scope
-   2. Reference eligibility
-   3. Reference records
-   4. Hunt definition
-   5. Candidate detection
-   6. Side mapping
-   7. Multiple reference resolution
-   8. Confirmation rule
-   9. Candidate invalidation before confirmation
-   10. Simultaneous buy and sell
-   11. Same-direction multiple signals

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06 - MQL5 Architecture Plan]] — `experiment`
- [[docs/evidence/07_test_plan/ad357cabb5f5_07_test_plan|07 - Test Plan]] — `experiment`
- [[docs/evidence/08_open_questions/18e20583bb82_08_open_questions|08 - Open Questions]] — `experiment`
- [[docs/evidence/09_owner_decisions_pass_1/d64c20e06d5e_09_owner_decisions_pass_1|09 - Owner Decisions Pass 1]] — `experiment`
- [[docs/evidence/11_algorithm_layers/07355f60fef2_11_algorithm_layers|11 - Algorithm Layers]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines|12 - State Machines]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13 - Data Model and Journals]] — `experiment`
- [[docs/evidence/14_backtest_live_runtime/c31f0574e3ec_14_backtest_live_runtime|14 - Backtest and Live Runtime]] — `experiment`
- [[docs/evidence/15_visualization_contract/0ccec648c2ec_15_visualization_contract|15 - Visualization Contract]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
