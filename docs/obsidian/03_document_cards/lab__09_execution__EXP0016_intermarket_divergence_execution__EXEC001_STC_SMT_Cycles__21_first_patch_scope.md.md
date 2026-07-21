---
title: "EXEC001 STC SMT Cycles — First Implementation Patch Scope"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "3223"
entities:
  - "EXEC001"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "Intermarket Divergence"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# EXEC001 STC SMT Cycles — First Implementation Patch Scope

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `3223` bytes

## خلاصه

This document defines the exact scope of the first code patch. The first patch must create a stable execution shell only. It must not implement SMT logic. Create a compilable MQL5 Expert Advisor and include structure that can host the STC SMT Cycles engine. The first patch should prove that the project structure, inputs, timer loop, symbol handling, runtime modes, output folder setup, and build sanity logs are stable. `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5` `mql5/Include/IntermarketDivergenceExecution/STC/` `DAL_STC_Enums.mqh` `DAL_STC_Types.mqh` `DAL_STC_Config.mqh` `DAL_STC_Utils.mqh` `DAL_STC_Journal.mqh` minimal stub `DAL_STC_Engine.mqh` minimal no-op

## Headings

- EXEC001 STC SMT Cycles — First Implementation Patch Scope
-   1. Objective
-   2. Files to Add
-     Expert
-     Include Directory
-     Include Files
-   3. Inputs to Add
-   4. Runtime Modes
-   5. Build Sanity Log
-   6. Validation Logic
-   7. Timer Loop
-   8. Output Folders

## Entities

`EXEC001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|Level 19 — Validation Pack / Self-Test Reports]] — `experiment`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_risk_register/b5f9b48975ee_20_implementation_risk_register|EXEC001 STC SMT Cycles — Implementation Risk Register]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|Level 09 — Paper Outcome Simulator and Trade Journal]] — `experiment`
- [[docs/evidence/level_11_paper_hard_close_simulator_15_30_end_day_accounting/d27b26fac569_32_level_11_hard_close_simulator|Level 11 — Paper Hard-Close Simulator and 15:30 End-of-Day Accounting]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|Level 14 — Paper Live Alerts / No-Order Monitoring Layer]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
