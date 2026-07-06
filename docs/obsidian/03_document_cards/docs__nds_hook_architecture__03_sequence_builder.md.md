---
title: "03 — Sequence Builder"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/03_sequence_builder.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "2081"
concepts:
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# 03 — Sequence Builder

**Source:** [[docs/nds_hook_architecture/03_sequence_builder|docs/nds_hook_architecture/03_sequence_builder.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `2081` bytes

## خلاصه

Build Hook / CycleHook sequences from NDS nodes. Every eligible node can start a CycleHook sequence, subject to the starter reuse rule. A node can be the starter of a sequence once. A node may appear in later positions of other sequences, but it should not repeatedly start new sequences after already serving as a starter. Positive sequence: Each new accepted X node must be lower than the previous accepted X node. Negative sequence: Each new accepted X node must be higher than the previous accepted X node. The system should allow multiple alive sequences at the same time. Each sequence keeps its own identity. Suggested object: If a sequence produces more than the allowed number of nodes, incr

## Headings

- 03 — Sequence Builder
-   Objective
-   Starter Rule
-   Positive Sequence Rule
-   Negative Sequence Rule
-   Multi-Sequence Rule
-   Max Nodes Rule
-   Fixed-Origin vs Recalculated-Origin Views
-     Fixed-Origin View
-     Recalculated-Origin View
-   Sequence Fields
-   Sequence Audit

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04 — X/Y Closure and Hook Types]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10 — Hook Phase 03 Implementation: Y-Axis Opposite Extremes]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|11 — Hook Phase 04 Implementation: ND, Death Lifecycle, and X Closure Skeleton]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/12_phase05_hook_type_abc_classifier_implementation|12 — Hook Phase 05 Implementation: Hook Type A/B/C Classifier]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
