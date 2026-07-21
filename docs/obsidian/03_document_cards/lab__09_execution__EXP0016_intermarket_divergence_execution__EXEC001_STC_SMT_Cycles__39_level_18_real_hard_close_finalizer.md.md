---
title: "Level 18 — Real Hard Close Finalizer"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "5321"
concepts:
  - "Convexity"
  - "Execution"
  - "Intermarket Divergence"
  - "NDS Anatomy"
  - "Validation"
---


# Level 18 — Real Hard Close Finalizer

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `5321` bytes

## خلاصه

Level 18 turns the 15:30 New York hard-close rule into a dedicated real broker finalizer. It does not change the STC signal logic, SMT detection, reference selection, paper simulator, real auto-entry router, or real partial close manager. Its only job is to make sure that, after the STC trading day ends, no remaining real broker position owned by this strategy instance is left open. The finalizer is magic-only. It manages only positions whose symbol is Symbol1 or Symbol2 and whose magic number equals the configured STC magic number. Manual positions, foreign-magic positions, and non-pair symbols are never closed by this module. The STC SRS requires all open STC trades to be closed at 15:30 N

## Headings

- Level 18 — Real Hard Close Finalizer
-   Purpose
-   Locked Strategy Rule Covered
-   Safety Defaults
-   Position Eligibility
-   Retry Model
-   Verification After Close Attempt
-   Audit Output
-   Relationship to Prior Layers
-   What Level 18 Still Does Not Do
-   Acceptance Criteria

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/36_level_15_broker_position_manager|Level 15 — Broker Position Manager / Magic-Only Safety Layer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|Level 19 — Validation Pack / Self-Test Reports]] — `experiment`
- [[docs/evidence/level_20_deployment_profile_matrix/97ecd654ebb6_42_level_20_profile_matrix|Level 20 — Deployment Profile Matrix]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06 - MQL5 Architecture Plan]] — `experiment`
- [[docs/evidence/07_test_plan/ad357cabb5f5_07_test_plan|07 - Test Plan]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
