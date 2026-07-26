---
title: "15 - Visualization Contract"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/15_visualization_contract/0ccec648c2ec_15_visualization_contract.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "2410"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Intermarket Divergence"
  - "Structural Nodes"
  - "Validation"
---


# 15 - Visualization Contract

**Source:** [[docs/evidence/15_visualization_contract/0ccec648c2ec_15_visualization_contract|docs/evidence/15_visualization_contract/0ccec648c2ec_15_visualization_contract.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `2410` bytes

## خلاصه

Visualization is required for audit, debugging, and human trust. It is not part of the decision engine. The drawing layer must never change signal logic. The EA can run on any chart. Drawings should be placed on the attached chart for audit, but the underlying logic still uses Symbol1 and Symbol2. Because a single chart can show only one symbol's price scale, drawings should support two modes: 1. Attached-chart mode: draw events related to the chart symbol if it is Symbol1 or Symbol2. 2. Audit-panel mode: draw textual event summaries regardless of chart symbol. All objects should use a safe prefix: `DAL_STC_EXEC001_` The renderer may delete and redraw only objects with this prefix. Cycle dra

## Headings

- 15 - Visualization Contract
-   1. Purpose
-   2. Chart independence
-   3. Drawing object prefix
-   4. Recommended drawings
-   5. Drawing defaults
-   6. Drawing density controls
-   7. No further strategy questions

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/11_algorithm_layers/07355f60fef2_11_algorithm_layers|11 - Algorithm Layers]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/43_level_21_drawing_audit|Level 21 — Drawing Audit Hardening + HardClose Warning Fix]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[docs/evidence/16_implementation_checklist/29731b650a84_16_implementation_checklist|16 - Implementation Checklist]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/23_level_02_time_engine|Level 02 — STC Time Engine and Cycle Classifier]] — `experiment`
- [[docs/evidence/level_03_check_candle_aggregator_pair_data_completeness/dad06b849807_24_level_03_check_candle_aggregator|Level 03 — Check Candle Aggregator and Pair Data Completeness]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/29_level_08_risk_plan_paper_entry|Level 08 — Risk Plan and No-Order Paper Entry Model]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
