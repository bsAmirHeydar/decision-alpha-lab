---
title: "Phase 18 — Minimal Readability / Qualified Hooks"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/26_phase18_minimal_readability_qualified_hooks.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "1606"
concepts:
  - "Hook"
  - "NDS Anatomy"
---


# Phase 18 — Minimal Readability / Qualified Hooks

**Source:** [[docs/nds_hook_architecture/26_phase18_minimal_readability_qualified_hooks|docs/nds_hook_architecture/26_phase18_minimal_readability_qualified_hooks.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `1606` bytes

## خلاصه

`MINIMAL_ALL_HOOKS` correctly removed the heavy P03/P04/P05/P06 overlays, but the chart was still visually busy because it rendered every raw candidate, including many `X1` structures. An `X1` structure is useful for raw debugging, but it is usually not a readable Hook. The arc height was also too large on high-range moves, and arrow-style X markers still added unnecessary visual weight. Phase 18 adds readability controls to Phase 02: `FP_HOOK_P07_VIEW_MINIMAL_ALL_HOOKS` now forces: So the view shows all **qualified** Hook sequences, not every one-node candidate. `X1` candidates are hidden by default. `X2+` Hook structures remain visible. Arcs are capped so they do not dominate the chart. No

## Headings

- Phase 18 — Minimal Readability / Qualified Hooks
-   Problem
-   Fix
-   Minimal profile defaults
-   Meaning
-   To show every raw candidate again

## Concepts

- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

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
