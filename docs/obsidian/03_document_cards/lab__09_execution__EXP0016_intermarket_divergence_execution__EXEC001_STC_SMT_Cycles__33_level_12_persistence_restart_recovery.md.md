---
title: "Level 12 — Persistence and Restart Recovery"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/33_level_12_persistence_restart_recovery.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "4593"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Level 12 — Persistence and Restart Recovery

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/33_level_12_persistence_restart_recovery|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/33_level_12_persistence_restart_recovery.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `4593` bytes

## خلاصه

Level 12 adds the first persistence layer for `EXEC001_STC_SMT_Cycles`. It does not place real orders, does not close real positions, and does not draw chart objects. Its purpose is to keep the paper/audit engine deterministic across EA restarts during the same STC trading day. The STC SRS requires the Expert Advisor to avoid duplicate trades for the same divergence and to reset all state at the end of the STC trading day. Owner clarification also locked that missed entries must not be executed late, delayed partial actions must be recovered, delayed hard close must be recovered, and only the current STC trading day may influence the current day. Level 12 is the first implementation layer th

## Headings

- Level 12 — Persistence and Restart Recovery
-   Scope
-   What is persisted
-   Snapshot file
-   Recovery audit file
-   Restore validation
-   Restore sequence
-   Snapshot write timing
-   Current limitation
-   Acceptance criteria

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/28_level_07_confirmation_signal_registry|Level 07 — Confirmation and Signal Registry]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/01_source_srs_extraction|01 - Source SRS Extraction]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06 - MQL5 Architecture Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/07_test_plan|07 - Test Plan]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
