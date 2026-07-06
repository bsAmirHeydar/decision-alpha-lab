---
title: "14 - Backtest and Live Runtime"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/14_backtest_live_runtime.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "3479"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "NDS Anatomy"
  - "Validation"
---


# 14 - Backtest and Live Runtime

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/14_backtest_live_runtime|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/14_backtest_live_runtime.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `3479` bytes

## خلاصه

The implementation should support three modes: 1. Research backtest. 2. Paper live. 3. Auto trade. The first build should prioritize research backtest and paper live. Auto trade should be enabled only after deterministic tests pass. Backtest loop: 1. Load Symbol1 and Symbol2 bars. 2. Convert timestamps to New York time. 3. Build STC trading days. 4. For each day, build M/W structure. 5. Build check candles anchored at 20:00. 6. Process completed check candles in chronological order. 7. Detect and confirm SMT. 8. Create simulated entries at next check-candle open. 9. Simulate SL/TP/ambiguous outcomes using check-candle bars. 10. Apply partial and hard close rules. 11. Write journals and summa

## Headings

- 14 - Backtest and Live Runtime
-   1. Runtime modes
-   2. Research backtest runtime
-   3. Backtest data requirements
-   4. Backtest entry timing
-   5. Backtest outcome timing
-   6. Paper live runtime
-   7. Auto-trade runtime
-   8. Live entry failure
-   9. Offline-at-entry behavior
-   10. Delayed actions allowed
-   11. Runtime safety rules

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
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines|12 - State Machines]] — `experiment`
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
