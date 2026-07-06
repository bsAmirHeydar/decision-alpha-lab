---
title: "Phase 21 — Cycle Arc Ends at the Directional Extreme"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/29_phase21_cycle_arc_directional_extreme.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "1498"
concepts:
  - "Hook"
  - "NDS Anatomy"
---


# Phase 21 — Cycle Arc Ends at the Directional Extreme

**Source:** [[docs/nds_hook_architecture/29_phase21_cycle_arc_directional_extreme|docs/nds_hook_architecture/29_phase21_cycle_arc_directional_extreme.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `1498` bytes

## خلاصه

Make the cycle semicircle match the intended Hook anatomy: the cycle arc starts at the Hook origin the arc spans toward the semicircle crown the arc endpoint lands where the cycle actually saw its directional extreme for a positive Hook, that endpoint is the **lowest valley seen by the cycle** for a negative Hook, that endpoint is the **highest peak seen by the cycle** The cycle arc ended at the **last visible X** (`X1`, `X2`, `X3`, or `X4`). That was acceptable for generic debugging, but it did not match the intended interpretation of the Hook cycle. A new Phase 02 setting was added: Modes: `FP_HOOK_P02_CYCLE_ARC_END_LAST_VISIBLE_X` `FP_HOOK_P02_CYCLE_ARC_END_DIRECTIONAL_EXTREME` When `DIRE

## Headings

- Phase 21 — Cycle Arc Ends at the Directional Extreme
-   Goal
-   Problem in previous versions
-   New arc endpoint mode
-   Directional extreme behavior
-   Minimal profile default

## Concepts

- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/01_scope_and_inputs|01 — Scope and Inputs]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/02_cyclehook_object_model|02 — CycleHook Object Model]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/03_sequence_builder|03 — Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04 — X/Y Closure and Hook Types]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05 — Visualization and Diagnostics]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10 — Hook Phase 03 Implementation: Y-Axis Opposite Extremes]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
