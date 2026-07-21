---
title: "Level 07 — Confirmation and Signal Registry"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/level_07_confirmation_signal_registry/c5f8b7b0b328_28_level_07_confirmation_signal_registry.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "4693"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Level 07 — Confirmation and Signal Registry

**Source:** [[docs/evidence/level_07_confirmation_signal_registry/c5f8b7b0b328_28_level_07_confirmation_signal_registry|docs/evidence/level_07_confirmation_signal_registry/c5f8b7b0b328_28_level_07_confirmation_signal_registry.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `4693` bytes

## خلاصه

Level 07 converts the audit-only SMT candidates from Level 06 into an audit-only signal registry. It still does not place paper trades and it still does not send real orders. This level is the first layer where the strategy speaks in terms of a confirmed STC signal rather than a raw hunt or a raw SMT candidate. The locked owner rule is that the signal only exists at the close of a valid check candle. If the expert was offline at that exact entry moment, the system must never enter later because the stop quality is no longer the same. Level 07 records such situations as audit-only consumed rows. `InpWriteSignalRegistryAudit` `InpMaxSignalBackfillOnInit` `InpMaxSignalCatchupPerPulse` These inp

## Headings

- Level 07 — Confirmation and Signal Registry
-   Purpose
-   Inputs Added
-   New MQL5 Module
-   New Output File
-   Signal Registry Rules
-   Confirmation Meaning
-   Entry OFF Rule
-   Offline / Late Entry Rule
-   Simultaneous Buy and Sell Rule
-   Final Check Candle Rule
-   Signal Consumption

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|EXEC001 STC SMT Cycles — Level 01 Skeleton Implementation]] — `experiment`
- [[docs/evidence/level_12_persistence_restart_recovery/965c940d2cdd_33_level_12_persistence_restart_recovery|Level 12 — Persistence and Restart Recovery]] — `experiment`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/evidence/01_source_srs_extraction/3916a86b9266_01_source_srs_extraction|01 - Source SRS Extraction]] — `experiment`
- [[docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06 - MQL5 Architecture Plan]] — `experiment`
- [[docs/evidence/07_test_plan/ad357cabb5f5_07_test_plan|07 - Test Plan]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
