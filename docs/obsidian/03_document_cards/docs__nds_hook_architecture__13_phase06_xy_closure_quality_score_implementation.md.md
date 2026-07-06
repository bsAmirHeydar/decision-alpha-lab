---
title: "13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "4401"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Rally"
  - "Structural Nodes"
  - "Validation"
---


# 13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score

**Source:** [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `4401` bytes

## خلاصه

Phase 06 adds an independent X/Y closure-strength and structural quality layer on top of Phase 05. It uses: This phase is still visualization and diagnostics only. Hook Type A/B/C is a global structural classifier. X/Y closure quality is a different layer: This separation is required because a Hook can be Type A/B/C while still having weak or incomplete internal X/Y closure. For positive CycleHook: Positive Y checks: For negative CycleHook: Negative Y checks: This is intentionally different from Hook Type A/B/C logic. Phase 06 reads the Phase 04 lifecycle fields: Default policy: So `XY_CLOSED` requires real Phase 04 `x_closed`, not just a candidate. Phase 06 emits: Meaning: Phase 06 computes

## Headings

- 13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score
-   Phase Goal
-   Why This Phase Exists
-   Y-Sequence Closure Logic
-   X Closure Input
-   XY Closure States
-   Quality Score
-   New MQL5 Modules
-   New Expert Inputs
-   Chart Objects
-   CSV Outputs
-   Preservation Rules

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation|Phase 09 — Visual Smoke Test Harness Implementation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation|Phase 10 — Hook v1 Freeze + Training Contract]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
