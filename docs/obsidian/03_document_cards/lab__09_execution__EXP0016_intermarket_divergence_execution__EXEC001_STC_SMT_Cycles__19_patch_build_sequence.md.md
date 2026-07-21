---
title: "EXEC001 STC SMT Cycles — Patch Build Sequence"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "5864"
entities:
  - "EXEC001"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "Intermarket Divergence"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# EXEC001 STC SMT Cycles — Patch Build Sequence

**Source:** [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `5864` bytes

## خلاصه

This document defines the exact engineering sequence for implementation patches. The purpose is to keep each patch small enough to compile, inspect, and debug. Create the EA shell and core types. EA file config structs enums inputs build sanity logs output folder creation timer loop no-op engine signal detection W logic order execution chart drawing beyond optional build label compiles with zero errors can attach to any chart prints all inputs confirms Symbol1 and Symbol2 exist Correctly classify New York time into STC day, M, W, gap, and hard-close zones. time conversion New York DST handling STC day object M/W schedule gap classifier final check candle classifier hard close classifier logs

## Headings

- EXEC001 STC SMT Cycles — Patch Build Sequence
-   Patch 001 — EA Skeleton, Inputs, and Build Sanity
-     Goal
-     Adds
-     Must Not Add
-     Acceptance
-   Patch 002 — Time and Cycle Engine
-     Goal
-     Adds
-     Acceptance
-   Patch 003 — Check Candle Aggregator
-     Goal

## Entities

`EXEC001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|Level 19 — Validation Pack / Self-Test Reports]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing]] — `execution_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|Level 09 — Paper Outcome Simulator and Trade Journal]] — `experiment`
- [[docs/evidence/level_11_paper_hard_close_simulator_15_30_end_day_accounting/d27b26fac569_32_level_11_hard_close_simulator|Level 11 — Paper Hard-Close Simulator and 15:30 End-of-Day Accounting]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|Level 14 — Paper Live Alerts / No-Order Monitoring Layer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/38_level_17_real_partial_close_manager|Level 17 — Real Partial Close Manager]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
