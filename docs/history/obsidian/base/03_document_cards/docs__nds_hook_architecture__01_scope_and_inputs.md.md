---
title: "01 — Scope and Inputs"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/01_scope_and_inputs.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "1588"
concepts:
  - "AI Agent Layer"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
  - "Validation"
---


# 01 — Scope and Inputs

**Source:** [[docs/nds_hook_architecture/01_scope_and_inputs|docs/nds_hook_architecture/01_scope_and_inputs.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `1588` bytes

## خلاصه

Add Hook visualization and diagnostics to the same central expert that already displays Rally / F-counting. The existing Rally behavior must remain untouched. Recommended input enum: The default should preserve existing behavior: This ensures that adding Hook code does not change the existing F-counting / Rally display. Use the current F-counting logic exactly as it is. No Hook code should change the Rally calculation path. Draw CycleHook / Hook objects and diagnostics. Do not draw Rally/F-counting labels unless they are explicitly needed for Hook debug. Draw both layers. Object names must be namespaced to avoid overwriting existing Rally chart objects. Suggested object prefixes: The first i

## Headings

- 01 — Scope and Inputs
-   Objective
-   Display Family Input
-   Suggested User Inputs
-   Default Behavior
-   Display Modes
-     Rally Only
-     Hook Only
-     Rally and Hook
-   Object Namespace
-   First Implementation Goal

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation|Phase 09 — Visual Smoke Test Harness Implementation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation|Phase 10 — Hook v1 Freeze + Training Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/37_phase26_doc_aligned_hook_rebuild|Phase 26 — Doc-Aligned Hook / ND Branch Rebuild]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/README|NDS Hook Architecture — Design Pack]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
