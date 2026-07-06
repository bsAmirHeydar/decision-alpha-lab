---
title: "06 - MQL5 Architecture Plan"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "5152"
concepts:
  - "Convexity"
  - "Execution"
  - "Intermarket Divergence"
  - "MQL Native"
  - "Validation"
---


# 06 - MQL5 Architecture Plan

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `5152` bytes

## خلاصه

The implementation must be modular. The STC strategy should not be a single large EA with hidden state. It should be built from reusable modules that can later support other SMT/cycle-divergence strategies. MQL5 experts: `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5` MQL5 include modules: `mql5/Include/IntermarketDivergenceExecution/Core/` `mql5/Include/IntermarketDivergenceExecution/STC/` STC modules: `DAL_STC_Types.mqh` `DAL_STC_Time.mqh` `DAL_STC_Cycles.mqh` `DAL_STC_CheckCandles.mqh` `DAL_STC_WLevels.mqh` `DAL_STC_SMTDetector.mqh` `DAL_STC_Confirmation.mqh` `DAL_STC_ReferenceSelector.mqh` `DAL_STC_Risk.mqh` `DAL_STC_PositionManager.mqh` `DAL_STC_StateJournal.

## Headings

- 06 - MQL5 Architecture Plan
-   1. Design goal
-   2. Proposed folder structure
-   3. Core modules
-   4. STC EA responsibilities
-   5. Scheduler algorithm
-   6. Time engine
-   7. Cycle engine
-   8. Check candle engine
-   9. SMT detector
-   10. Confirmation and filter pipeline
-   11. Risk module

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|Level 20 — Operator Manual and Deployment Profiles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/08_open_questions|08 - Open Questions]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers|11 - Algorithm Layers]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/20_implementation_risk_register|EXEC001 STC SMT Cycles — Implementation Risk Register]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector|Level 05 — Reference Matrix and Raw Hunt Detector]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
