---
title: "NDS Hook Official Schematic Visual Cleanup"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/18_phase11_official_schematic_visual_cleanup.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "2144"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
---


# NDS Hook Official Schematic Visual Cleanup

**Source:** [[docs/nds_hook_architecture/18_phase11_official_schematic_visual_cleanup|docs/nds_hook_architecture/18_phase11_official_schematic_visual_cleanup.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `2144` bytes

## خلاصه

The raw multi-phase Hook overlay was technically correct for debugging, but visually too noisy for the official structural reading. The main pollution came from: projecting lifecycle thresholds all the way to `TimeCurrent()` stacking full debug labels from Phase 05 and Phase 06 leaving the Phase 07 view profile on permissive modes such as `KEEP_INPUTS` drawing too many structures at once A new Phase 07 view profile was added: `FP_HOOK_P07_VIEW_OFFICIAL_SCHEMATIC` This profile draws a clean Hook schematic: Phase 02: origin + X nodes + X lines Phase 03: Y extremes + Y lines Phase 04: ND / death / X-close markers only Phase 05: compact Hook type anchor + compact type label Phase 06: compact qua

## Headings

- NDS Hook Official Schematic Visual Cleanup
-   Why
-   What changed
-     1) New official visual profile
-     2) New clean defaults
-     3) Threshold-line fix
-     4) Compact labels
-   Recommended usage

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/01_scope_and_inputs|01 — Scope and Inputs]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/02_cyclehook_object_model|02 — CycleHook Object Model]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04 — X/Y Closure and Hook Types]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10 — Hook Phase 03 Implementation: Y-Axis Opposite Extremes]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
