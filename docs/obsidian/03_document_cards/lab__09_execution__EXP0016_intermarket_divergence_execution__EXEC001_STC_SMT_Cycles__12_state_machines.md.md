---
title: "12 - State Machines"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "2992"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "NDS Anatomy"
  - "Validation"
---


# 12 - State Machines

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `2992` bytes

## خلاصه

States: `BEFORE_STC_DAY` `ACTIVE_DAY` `HARD_CLOSE_DUE` `HARD_CLOSE_RECOVERY` `DAY_RESET_DONE` Transitions: At 20:00 New York, enter `ACTIVE_DAY`. At 15:30 New York, enter `HARD_CLOSE_DUE`. If all STC positions close successfully, enter `DAY_RESET_DONE`. If any close fails or EA restarts after 15:30 with open STC positions, enter `HARD_CLOSE_RECOVERY`. After successful recovery, reset state for next day. States: `NOT_STARTED` `ACTIVE` `GAP_AFTER_M` `ENDED` M state carries: M ID. Trade count. Direction lock. Opened trade IDs. Partial due time. On M start: Trade count = 0. Direction lock = none. On first opened trade when Hedging OFF: Direction lock = trade side. On M end: No more entries allow

## Headings

- 12 - State Machines
-   1. Strategy day state
-   2. M state
-   3. W state
-   4. Candidate state
-   5. Trade state
-   6. Partial state
-   7. Hard-close state

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/07_test_plan|07 - Test Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/14_backtest_live_runtime|14 - Backtest and Live Runtime]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/23_level_02_time_engine|Level 02 — STC Time Engine and Cycle Classifier]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/24_level_03_check_candle_aggregator|Level 03 — Check Candle Aggregator and Pair Data Completeness]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/28_level_07_confirmation_signal_registry|Level 07 — Confirmation and Signal Registry]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
