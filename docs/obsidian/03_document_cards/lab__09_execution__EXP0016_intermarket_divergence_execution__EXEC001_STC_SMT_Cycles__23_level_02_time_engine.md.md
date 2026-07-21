---
title: "Level 02 — STC Time Engine and Cycle Classifier"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/23_level_02_time_engine.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "4956"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# Level 02 — STC Time Engine and Cycle Classifier

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/23_level_02_time_engine|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/23_level_02_time_engine.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `4956` bytes

## خلاصه

Status: implemented in patch `EXP0016_STC_SMT_LEVEL02_TIME_ENGINE`. This level is still a no-trade layer. It does not build W highs/lows, does not detect SMT divergence, does not create signals, and does not send orders. Its only responsibility is to convert the terminal time into the canonical STC time model and to produce an auditable time/cycle stream. The STC strategy is entirely time-driven. Every later decision depends on the correct New York trading-day classification: Whether the current moment belongs to the STC trading day. Whether the current moment is inside M1, M2, M3, or a no-entry gap. Which W cycle is active. Whether the current check candle is the final check candle of an M,

## Headings

- Level 02 — STC Time Engine and Cycle Classifier
-   Why this level exists
-   Canonical time model
-   STC trading day
-   M cycle classification
-   W cycle classification
-   Check-candle anchoring
-   Final check candle rule
-   Audit output
-   Acceptance criteria
-   Next level

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[docs/evidence/level_03_check_candle_aggregator_pair_data_completeness/dad06b849807_24_level_03_check_candle_aggregator|Level 03 — Check Candle Aggregator and Pair Data Completeness]] — `experiment`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|Level 19 — Validation Pack / Self-Test Reports]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[docs/evidence/07_test_plan/ad357cabb5f5_07_test_plan|07 - Test Plan]] — `experiment`
- [[docs/evidence/11_algorithm_layers/07355f60fef2_11_algorithm_layers|11 - Algorithm Layers]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines|12 - State Machines]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
