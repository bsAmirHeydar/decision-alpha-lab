---
title: "02 — CycleHook Object Model"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/02_cyclehook_object_model.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "2169"
concepts:
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
---


# 02 — CycleHook Object Model

**Source:** [[docs/nds_hook_architecture/02_cyclehook_object_model|docs/nds_hook_architecture/02_cyclehook_object_model.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `2169` bytes

## خلاصه

Hook and CycleHook are the same algorithmic object. Recommended canonical object: There are two directions: A positive CycleHook starts from a valley. Its counted X nodes are valleys. The sequence is strictly lower valleys. Equal nodes are not accepted as new lower nodes. A negative CycleHook starts from a peak. Its counted X nodes are peaks. The sequence is strictly higher peaks. Equal nodes are not accepted as new higher nodes. One-point penetration of the origin kills the CycleHook. There is no structural buffer for validity. Execution buffer may exist later, but structural validity is strict. For a positive CycleHook, opposite Extremes are highs. For a negative CycleHook, opposite Extrem

## Headings

- 02 — CycleHook Object Model
-   Canonical Rule
-   Directions
-   Positive CycleHook
-   Negative CycleHook
-   Death Rule
-   Opposite Extreme
-   Minimum L
-   CycleHook Fields
-   Lifecycle States

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation|Phase 09 — Visual Smoke Test Harness Implementation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation|Phase 10 — Hook v1 Freeze + Training Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/18_phase11_official_schematic_visual_cleanup|NDS Hook Official Schematic Visual Cleanup]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/README|NDS Hook Architecture — Design Pack]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
