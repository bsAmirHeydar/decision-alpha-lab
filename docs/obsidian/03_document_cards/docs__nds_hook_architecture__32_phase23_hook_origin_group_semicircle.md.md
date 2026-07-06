---
title: "Phase 23 — Hook-Origin Grouped Cycle Semicircle"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/32_phase23_hook_origin_group_semicircle.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "1381"
concepts:
  - "Hook"
  - "NDS Anatomy"
---


# Phase 23 — Hook-Origin Grouped Cycle Semicircle

**Source:** [[docs/nds_hook_architecture/32_phase23_hook_origin_group_semicircle|docs/nds_hook_architecture/32_phase23_hook_origin_group_semicircle.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `1381` bytes

## خلاصه

The previous implementation still drew a cycle arc **per sequence**. Even with straight X-lines disabled, this produced multiple overlapping arc traces that visually looked like node-to-node connections. That is not the intended Hook schematic. Node numbering should show **all sequences**. But the cycle semicircle should represent the **Hook envelope**, not each inner sequence leg separately. Therefore the cycle arc should be drawn **once per Hook origin group**. A Hook-origin group is defined by: `direction` `origin_time` `origin_price` All selected sequences that share those fields belong to the same Hook envelope group. For each origin group: start = Hook origin end = directional extreme

## Headings

- Phase 23 — Hook-Origin Grouped Cycle Semicircle
-   Problem
-   Intended semantics
-   Grouping rule
-   Group arc endpoint
-   Rendering behavior
-   New input

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
