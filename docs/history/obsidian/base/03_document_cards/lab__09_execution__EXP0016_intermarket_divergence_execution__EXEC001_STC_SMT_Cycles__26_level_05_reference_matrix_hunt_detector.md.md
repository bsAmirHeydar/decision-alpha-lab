---
title: "Level 05 — Reference Matrix and Raw Hunt Detector"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "5898"
concepts:
  - "Convexity"
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# Level 05 — Reference Matrix and Raw Hunt Detector

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `5898` bytes

## خلاصه

Level 05 adds the first market-condition detector for `EXEC001_STC_SMT_Cycles`. It does **not** create SMT candidates yet. It does **not** confirm signals. It does **not** simulate trades. It does **not** place orders. This level only answers one question for every closed check candle: > Against each legal previous-W reference inside the same M, did Symbol1 and/or Symbol2 touch the reference high or low? The output is a raw reference-hunt audit stream. Later levels will convert these raw hunts into SMT divergence candidates, then confirmation events, then paper trades, then optional live orders. Level 05 implements these locked rules: W1 never produces a signal. W2 may compare only with W1.

## Headings

- Level 05 — Reference Matrix and Raw Hunt Detector
-   Purpose
-   Locked owner rules implemented in this level
-   Reference matrix
-   Raw hunt definitions
-     Symbol1 high hunt
-     Symbol1 low hunt
-     Symbol2 high hunt
-     Symbol2 low hunt
-   Hunt patterns
-   Why Level 05 does not create SMT signals yet
-   Output file

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06 - MQL5 Architecture Plan]] — `experiment`
- [[docs/evidence/08_open_questions/18e20583bb82_08_open_questions|08 - Open Questions]] — `experiment`
- [[docs/evidence/11_algorithm_layers/07355f60fef2_11_algorithm_layers|11 - Algorithm Layers]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/36_level_15_broker_position_manager|Level 15 — Broker Position Manager / Magic-Only Safety Layer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer|Level 18 — Real Hard Close Finalizer]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|Level 19 — Validation Pack / Self-Test Reports]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|Level 20 — Operator Manual and Deployment Profiles]] — `experiment`
- [[docs/evidence/level_20_deployment_profile_matrix/97ecd654ebb6_42_level_20_profile_matrix|Level 20 — Deployment Profile Matrix]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
