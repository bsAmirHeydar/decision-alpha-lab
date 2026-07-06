---
title: "NDS Hook Phase 12 — Update Cleanup Contract"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/19_phase12_update_cleanup_contract.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "1620"
concepts:
  - "AI Agent Layer"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# NDS Hook Phase 12 — Update Cleanup Contract

**Source:** [[docs/nds_hook_architecture/19_phase12_update_cleanup_contract|docs/nds_hook_architecture/19_phase12_update_cleanup_contract.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `1620` bytes

## خلاصه

When the expert updates, the previous Hook drawings must not remain on the chart. The chart must represent the current calculation pass only. Phase 07 cleanup is now extended from P01..P07 to the full Hook overlay namespace P01..P10. A common prefix cleanup was also added: `InpHookPhase07CleanCommonHookPrefix` `InpHookPhase07CommonHookObjectPrefix = "DAL_HOOK_"` This deletes stale objects from older Hook phases or previous prefixes before the current pass redraws. New cleanup toggles: `InpHookPhase07CleanP08Objects` `InpHookPhase07CleanP09Objects` `InpHookPhase07CleanP10Objects` All are enabled by default. Phase 07 now also stores the cleanup prefixes for: Phase 08 audit objects / future obj

## Headings

- NDS Hook Phase 12 — Update Cleanup Contract
-   Purpose
-   Change
-   Runtime behavior
-   Default

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/01_scope_and_inputs|01 — Scope and Inputs]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10 — Hook Phase 03 Implementation: Y-Axis Opposite Extremes]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|11 — Hook Phase 04 Implementation: ND, Death Lifecycle, and X Closure Skeleton]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/37_phase26_doc_aligned_hook_rebuild|Phase 26 — Doc-Aligned Hook / ND Branch Rebuild]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
