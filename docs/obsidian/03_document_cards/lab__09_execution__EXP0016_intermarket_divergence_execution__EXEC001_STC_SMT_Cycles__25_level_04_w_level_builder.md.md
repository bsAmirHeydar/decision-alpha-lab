---
title: "Level 04 — W Level Builder"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/25_level_04_w_level_builder.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "3318"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# Level 04 — W Level Builder

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/25_level_04_w_level_builder|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/25_level_04_w_level_builder.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `3318` bytes

## خلاصه

Level 04 adds the first structural market object required by STC: the closed 90-minute W high/low levels for both symbols. This level is still non-trading. It does not detect SMT, confirm signals, simulate entries, draw objects, open positions, partial-close positions, or hard-close positions. It only builds and audits W levels after each W closes. STC does not compare raw prices between SPX and NDX. It compares each symbol against its own W reference levels. Therefore the system needs a deterministic W-level layer before SMT can exist. The locked owner rule is: each symbol has its own W high and W low; the comparison is structural, not price-shared; W1 gives no signal; W2 may later compare

## Headings

- Level 04 — W Level Builder
-   Status
-   Why this level exists
-   Output file
-   W serial map
-   Completeness rule
-   Reference role
-   Level 04 acceptance criteria

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
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13 - Data Model and Journals]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/14_backtest_live_runtime|14 - Backtest and Live Runtime]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
