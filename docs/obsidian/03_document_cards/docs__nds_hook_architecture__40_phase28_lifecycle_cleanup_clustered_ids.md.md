---
title: "Phase 28 — Lifecycle Cleanup and Clustered Hook/Branch Label IDs"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/40_phase28_lifecycle_cleanup_clustered_ids.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "2509"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
---


# Phase 28 — Lifecycle Cleanup and Clustered Hook/Branch Label IDs

**Source:** [[docs/nds_hook_architecture/40_phase28_lifecycle_cleanup_clustered_ids|docs/nds_hook_architecture/40_phase28_lifecycle_cleanup_clustered_ids.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `2509` bytes

## خلاصه

Fix two operational issues in the minimal Hook semantic view: 1. stale Hook objects must be removed when the timeframe changes, the chart identity changes, or the expert is reattached; 2. branch-number labels must be readable, stacked deterministically below valleys and above peaks, and carry minimal Hook/branch identity. The expert already had cleanup toggles, but Phase 28 hardens lifecycle cleanup by deleting the generic `DAL_HOOK_` namespace in addition to all configured Hook phase prefixes. This handles stale objects from: timeframe changes; expert remove / reattach; recompilation; parameter changes; older Hook profile prefixes; changed input prefixes. A runtime chart-identity guard was

## Headings

- Phase 28 — Lifecycle Cleanup and Clustered Hook/Branch Label IDs
-   Goal
-   Cleanup behavior
-   Label identity
-   Label clustering
-   Vertical placement
-   Rendering order

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10 — Hook Phase 03 Implementation: Y-Axis Opposite Extremes]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/12_phase05_hook_type_abc_classifier_implementation|12 — Hook Phase 05 Implementation: Hook Type A/B/C Classifier]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04 — X/Y Closure and Hook Types]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05 — Visualization and Diagnostics]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|11 — Hook Phase 04 Implementation: ND, Death Lifecycle, and X Closure Skeleton]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
