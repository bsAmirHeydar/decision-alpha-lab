---
title: "01 - Source SRS Extraction"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/01_source_srs_extraction/3916a86b9266_01_source_srs_extraction.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "6464"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "MQL Native"
  - "NDS Anatomy"
---


# 01 - Source SRS Extraction

**Source:** [[docs/evidence/01_source_srs_extraction/3916a86b9266_01_source_srs_extraction|docs/evidence/01_source_srs_extraction/3916a86b9266_01_source_srs_extraction.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `6464` bytes

## خلاصه

This file is a factual English extraction from `STC Expert Advisor SRS.pdf`. It does not add trading assumptions beyond the source. Implementation interpretations and unresolved questions are handled in later files. Expert Advisor name: `STC Expert Advisor`. Purpose: automate the STC strategy based on SMT divergence between two tradable indices. The strategy must only use information from the current trading day. No prior-day information should be used in decision-making after the daily reset. The EA is attached only once, on one chart. The chart symbol does not affect EA logic. All analysis is performed only on two input symbols. All trade management is also limited to those two symbols. ST

## Headings

- 01 - Source SRS Extraction
-   1. Project identity
-   2. General architecture
-   3. STC trading day
-   4. Time management
-   5. M cycles
-   6. W cycles
-     M1 W cycles
-     M2 W cycles
-     M3 W cycles
-   7. Inputs
-   8. SMT divergence definition

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/evidence/08_open_questions/18e20583bb82_08_open_questions|08 - Open Questions]] — `experiment`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/principles|Research Principles]] — `core_docs`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation]] — `experiment`
- [[docs/evidence/level_07_confirmation_signal_registry/c5f8b7b0b328_28_level_07_confirmation_signal_registry|Level 07 — Confirmation and Signal Registry]] — `experiment`
- [[docs/evidence/level_12_persistence_restart_recovery/965c940d2cdd_33_level_12_persistence_restart_recovery|Level 12 — Persistence and Restart Recovery]] — `experiment`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
