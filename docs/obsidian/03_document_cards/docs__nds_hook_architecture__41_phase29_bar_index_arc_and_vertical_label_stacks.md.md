---
title: "Phase 29 — Bar-Index Arc Timing and Vertical Label Stacks"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/41_phase29_bar_index_arc_and_vertical_label_stacks.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "1378"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Hook"
  - "NDS Anatomy"
---


# Phase 29 — Bar-Index Arc Timing and Vertical Label Stacks

**Source:** [[docs/nds_hook_architecture/41_phase29_bar_index_arc_and_vertical_label_stacks|docs/nds_hook_architecture/41_phase29_bar_index_arc_and_vertical_label_stacks.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `1378` bytes

## خلاصه

Fix two visual issues in the minimal Hook view: 1. Hook envelope curves should be laid out by candle progression rather than naive wall-clock interpolation, so the arc follows chart bar spacing more faithfully and does not visually break across session gaps. 2. Hook/branch labels should stack in cleaner vertical columns above peaks and below valleys instead of colliding on top of each other. The Hook envelope renderer now prefers bar-index aligned interpolation. start, crown, and end anchor times are converted to chart bar shifts the curve is sampled along bar progression between those anchors each short trend segment is anchored on actual chart bar times This makes the gray Hook envelope fo

## Headings

- Phase 29 — Bar-Index Arc Timing and Vertical Label Stacks
-   Goal
-   Changes
-     1) Arc timing aligned to bar index
-     2) Stronger label clustering
-   New config knobs
-   Default profile updates

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05 — Visualization and Diagnostics]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10 — Hook Phase 03 Implementation: Y-Axis Opposite Extremes]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/12_phase05_hook_type_abc_classifier_implementation|12 — Hook Phase 05 Implementation: Hook Type A/B/C Classifier]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/40_phase28_lifecycle_cleanup_clustered_ids|Phase 28 — Lifecycle Cleanup and Clustered Hook/Branch Label IDs]] — `nds_hook_architecture_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/01_scope_and_inputs|01 — Scope and Inputs]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04 — X/Y Closure and Hook Types]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
