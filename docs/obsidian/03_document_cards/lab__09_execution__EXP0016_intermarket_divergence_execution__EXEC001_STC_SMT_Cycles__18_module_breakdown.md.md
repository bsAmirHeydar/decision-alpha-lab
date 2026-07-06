---
title: "EXEC001 STC SMT Cycles — Module Breakdown"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "8075"
entities:
  - "EXEC001"
concepts:
  - "Convexity"
  - "Execution"
  - "Intermarket Divergence"
  - "Known-Time Causality"
  - "MQL Native"
  - "Structural Nodes"
  - "Validation"
---


# EXEC001 STC SMT Cycles — Module Breakdown

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `8075` bytes

## خلاصه

This document maps the strategy into concrete MQL5 modules. The implementation must avoid a monolithic EA. Each module must have one clear responsibility and must be independently testable through logs, audit CSVs, or deterministic replay. `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5` The EA entry point owns the lifecycle only: parse inputs initialize config initialize modules set timer route runtime events call the engine deinitialize cleanly The EA file should not contain strategy logic. `OnInit()` `OnDeinit()` `OnTimer()` optional `OnTick()` only as a wake-up mechanism `DAL_STC_Types.mqh` `DAL_STC_Enums.mqh` `DAL_STC_Config.mqh` Define all shared types. Core

## Headings

- EXEC001 STC SMT Cycles — Module Breakdown
-   1. Expert Advisor Entry Point
-     File
-     Responsibility
-     Main Functions
-   2. Types and Configuration
-     Files
-     Responsibility
-   3. Time Module
-     File
-     Responsibility
-   4. Cycle Module

## Entities

`EXEC001`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/20_implementation_risk_register|EXEC001 STC SMT Cycles — Implementation Risk Register]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|Level 19 — Validation Pack / Self-Test Reports]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation]] — `experiment`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/00_strategy_document_map|00 - Strategy Document Map]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/09_owner_decisions_pass_1|09 - Owner Decisions Pass 1]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|Level 09 — Paper Outcome Simulator and Trade Journal]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
