---
title: "Phase 25 — True Hook Arc and Extremum-Side Label Stacking"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/35_phase25_true_hook_arc_and_extremum_label_stacking.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "1270"
concepts:
  - "AI Agent Layer"
  - "Hook"
  - "NDS Anatomy"
---


# Phase 25 — True Hook Arc and Extremum-Side Label Stacking

**Source:** [[docs/nds_hook_architecture/35_phase25_true_hook_arc_and_extremum_label_stacking|docs/nds_hook_architecture/35_phase25_true_hook_arc_and_extremum_label_stacking.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `1270` bytes

## خلاصه

Fix the remaining mismatch in the minimal Hook view: sequence labels should not overlap labels should stack **below valleys** and **above peaks** the Hook line should be the **Hook envelope arc**, not anything that reads like node-to-node sequence wiring Node-number label placement now uses local point shape instead of Hook direction alone. valley-like nodes -> labels stack below the node peak-like nodes -> labels stack above the node Collision stacking also keys by time, side, and a small price bucket, so close labels on the same swing stack more reliably. The old grouped curve still used a generic smooth curve that could visually resemble a connection overlay. Now the grouped Hook curve is

## Headings

- Phase 25 — True Hook Arc and Extremum-Side Label Stacking
-   Goal
-   What changed
-     1) Extremum-side label stacking
-     2) True Hook envelope arc through the Hook crown

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/05_visualization/LABEL_STACKING|Label Stacking]] — `flag_counting_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/01_scope_and_inputs|01 — Scope and Inputs]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04 — X/Y Closure and Hook Types]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05 — Visualization and Diagnostics]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10 — Hook Phase 03 Implementation: Y-Axis Opposite Extremes]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|11 — Hook Phase 04 Implementation: ND, Death Lifecycle, and X Closure Skeleton]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/12_phase05_hook_type_abc_classifier_implementation|12 — Hook Phase 05 Implementation: Hook Type A/B/C Classifier]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
