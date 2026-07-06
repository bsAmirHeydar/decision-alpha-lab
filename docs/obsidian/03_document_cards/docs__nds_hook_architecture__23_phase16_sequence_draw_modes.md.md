---
title: "Phase 16 — Sequence Draw Modes"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/23_phase16_sequence_draw_modes.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "1706"
concepts:
  - "AI Agent Layer"
  - "Hook"
  - "NDS Anatomy"
---


# Phase 16 — Sequence Draw Modes

**Source:** [[docs/nds_hook_architecture/23_phase16_sequence_draw_modes|docs/nds_hook_architecture/23_phase16_sequence_draw_modes.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `1706` bytes

## خلاصه

Phase 15 made the sequence inspector too strict by hard-capping `SEQUENCE_CYCLE_DEBUG` to a single sequence. That solved clutter, but it also hid the surrounding sequence-counting context. Phase 16 adds explicit draw modes so the Hook inspector can show more than one sequence without returning to the previous P05/P06/P04 label pileup. Modes: Direction filter: Scale filter: `SEQUENCE_CYCLE_DEBUG` no longer hard-caps visible sequences to 1. It uses `InpHookPhase07MaxSequencesToDraw` and Phase 02 draw-mode filters while still hard-disabling P03/P04/P05/P06 drawing.

## Headings

- Phase 16 — Sequence Draw Modes
-   Reason
-   New Phase 02 input
-   Supporting inputs
-   Recommended views
-     Balanced context
-     One scale inspection
-     Exact sequence inspection
-   Phase 07 interaction

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

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
