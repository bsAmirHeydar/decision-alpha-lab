---
title: "Phase 17 — Minimal All Hooks View"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/25_phase17_minimal_all_hooks_view.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "1541"
concepts:
  - "AI Agent Layer"
  - "Hook"
  - "NDS Anatomy"
---


# Phase 17 — Minimal All Hooks View

**Source:** [[docs/nds_hook_architecture/25_phase17_minimal_all_hooks_view|docs/nds_hook_architecture/25_phase17_minimal_all_hooks_view.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `1541` bytes

## خلاصه

Show all Hook sequences in a minimal structural rendering: all Hook sequences sequence arc + path node markers only node numbers on chart node/line/arc colors derived from sequence color no long labels, no quality/type overlays, no thresholds This profile keeps only Phase 02 visible and disables Phase 03 through Phase 06. When `MINIMAL_ALL_HOOKS` is active: `Phase 02` remains enabled `draw_origin = true` `draw_x_nodes = true` `draw_x_lines = true` `draw_cycle_arc = true` `draw_sequence_count_label = false` `draw_labels = true` `use_sequence_palette_colors = true` `color_origin_with_sequence = true` `color_node_labels_with_sequence = true` `minimal_numbers_only = true` `node_label_mode = NUMB

## Headings

- Phase 17 — Minimal All Hooks View
-   Goal
-   New view profile
-   Minimal view behavior
-   New Phase 02 visual controls
-   Recommended inputs

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

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
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
