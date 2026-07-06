
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals.md"
source_ext: ".md"
source_size: 4378
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 13_data_model_and_journals.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals.md]]

## Summary

The strategy must be restart-safe, auditable, and testable. Every important decision should produce a record. The engine should be able to answer why it entered, why it skipped, why it rejected, and how it calculated SL/TP/volume. Fields: `stc_day_id` `ny_start_time` `ny_end_time` `hard_close_time` `symbol1` `symbol2` `broker_utc_offset` `check_candle_tf` `entry_stc_enabled` `partial_enabled` `hedging_enabled` Fields: `stc_day_id` `m_id` `start_time_ny` `end_time_ny` `trade_count` `direction_lock` `partial_due_time` `status` Fields: `stc_day_id` `m_id` `w_id` `symbol` `start_time_ny` `end_time_ny` `open` `high` `low` `close` `data_complete` `missing_bar_count` Fields: `stc_day_id` `check_close_time_ny` `check_start_time_ny` `check_tf` `m_id` `w_id` `is_final_check_candle_of_m` `symbol1_ohlc` `symbol2_ohlc` `data_complete` Fields: `candidate_id` `stc_day_id` `m_id` `current_w_id` `check_c

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 13 - Data Model and Journals
  - 1. Goals
  - 2. Core records
    - STC day record
    - M cycle record
    - W cycle record
    - Check candle record
    - SMT candidate record
    - Trade intent record
    - Trade journal record
  - 3. CSV outputs
    - `stc_cycle_audit.csv`

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk|05_execution_and_risk.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/16_implementation_checklist|16_implementation_checklist.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|19_patch_build_sequence.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
