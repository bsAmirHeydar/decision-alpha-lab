---
title: "08 — Hook Phase 01 Implementation: Node Source Adapter"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "2471"
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


# 08 — Hook Phase 01 Implementation: Node Source Adapter

**Source:** [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `2471` bytes

## خلاصه

This phase adds the first modular Hook/CycleHook implementation layer to the central expert. It does not implement full Hook sequences yet. It implements: New input: Values: Default: This preserves existing Rally/F-counting behavior by default. Phase 01 is not the full Hook algorithm. It is the Node Source Adapter for Hook. It answers: Peak: Valley: Equal highs/lows are rejected. Minimum L is forced to 2 for this layer. Enabled with: Outputs: Object prefix: Markers: Rally-only mode: Hook-only mode: Rally-and-Hook mode: This phase does not add:

## Headings

- 08 — Hook Phase 01 Implementation: Node Source Adapter
-   Scope
-   Display Family
-   Phase 01 Meaning
-   Strict Node Rules
-   New Modules
-   New CSV Outputs
-   New Chart Objects
-   Acceptance Criteria
-   No Execution Boundary

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
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
