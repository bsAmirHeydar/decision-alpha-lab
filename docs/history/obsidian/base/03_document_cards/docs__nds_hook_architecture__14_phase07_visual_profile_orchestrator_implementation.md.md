---
title: "14 — NDS Hook Phase 07: Visual Profile Orchestrator"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "6625"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Rally"
  - "Validation"
---


# 14 — NDS Hook Phase 07: Visual Profile Orchestrator

**Source:** [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `6625` bytes

## خلاصه

Phase 07 adds a central view-control layer for the Hook stack. The previous phases are now structurally independent: That modularity is correct, but it creates a chart-management problem: if all phases draw at the same time, the chart becomes noisy and stale objects from a previous view can remain visible after a profile switch. Phase 07 solves that problem by adding a single **view-profile orchestrator**. It does not build new Hook objects and it does not change the Rally/F-counting logic. It only transforms the already existing Phase 01..Phase 06 configs before those phases run. Phase 07 is still diagnostics and visualization infrastructure only. Forbidden in this phase: The central expert

## Headings

- 14 — NDS Hook Phase 07: Visual Profile Orchestrator
-   Purpose
-   Non-execution boundary
-   New files
-   Central expert integration
-   Inputs
-   View profiles
-     KEEP_INPUTS
-     RAW_NODES
-     SEQUENCE_XY
-     LIFECYCLE
-     TYPE_QUALITY

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation|Phase 09 — Visual Smoke Test Harness Implementation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation|Phase 10 — Hook v1 Freeze + Training Contract]] — `nds_hook_architecture_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|BASE-06 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
