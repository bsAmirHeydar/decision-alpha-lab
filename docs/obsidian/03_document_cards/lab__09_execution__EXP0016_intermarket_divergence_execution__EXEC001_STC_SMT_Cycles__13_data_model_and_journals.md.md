---
title: "13 - Data Model and Journals"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "4378"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# 13 - Data Model and Journals

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `4378` bytes

## خلاصه

The strategy must be restart-safe, auditable, and testable. Every important decision should produce a record. The engine should be able to answer why it entered, why it skipped, why it rejected, and how it calculated SL/TP/volume. Fields: `stc_day_id` `ny_start_time` `ny_end_time` `hard_close_time` `symbol1` `symbol2` `broker_utc_offset` `check_candle_tf` `entry_stc_enabled` `partial_enabled` `hedging_enabled` Fields: `stc_day_id` `m_id` `start_time_ny` `end_time_ny` `trade_count` `direction_lock` `partial_due_time` `status` Fields: `stc_day_id` `m_id` `w_id` `symbol` `start_time_ny` `end_time_ny` `open` `high` `low` `close` `data_complete` `missing_bar_count` Fields: `stc_day_id` `check_clo

## Headings

- 13 - Data Model and Journals
-   1. Goals
-   2. Core records
-     STC day record
-     M cycle record
-     W cycle record
-     Check candle record
-     SMT candidate record
-     Trade intent record
-     Trade journal record
-   3. CSV outputs
-     `stc_cycle_audit.csv`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/04_smt_divergence_rules|04 - SMT Divergence Rules and Algorithms]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06 - MQL5 Architecture Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/07_test_plan|07 - Test Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/08_open_questions|08 - Open Questions]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/09_owner_decisions_pass_1|09 - Owner Decisions Pass 1]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers|11 - Algorithm Layers]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines|12 - State Machines]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/14_backtest_live_runtime|14 - Backtest and Live Runtime]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/15_visualization_contract|15 - Visualization Contract]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
