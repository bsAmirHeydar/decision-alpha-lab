---
title: "Phase 27 — Lifecycle-Aligned Confirmed Near-Death Hook Visibility"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/39_phase27_lifecycle_confirmed_near_death_visibility.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "2566"
concepts:
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Phase 27 — Lifecycle-Aligned Confirmed Near-Death Hook Visibility

**Source:** [[docs/nds_hook_architecture/39_phase27_lifecycle_confirmed_near_death_visibility|docs/nds_hook_architecture/39_phase27_lifecycle_confirmed_near_death_visibility.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `2566` bytes

## خلاصه

The Phase 26 rebuild aligned the branch builder with the Hook/ND branch documentation, but the semantic renderer was still too permissive: a Hook could still visually span across its own floor/ceiling boundary; unconfirmed final nodes could still produce visible structure; arcs could be drawn before the last same-side node was confirmed in the Near-Death area; the renderer was still allowed to infer an end point from counted nodes instead of the confirmed lifecycle resolve node. This contradicts the lifecycle rule: > If the Hook floor/ceiling is touched or penetrated, the Hook is failed/dead. > If the final node is confirmed in Near-Death, draw only to that node. > If it is not confirmed, do

## Headings

- Phase 27 — Lifecycle-Aligned Confirmed Near-Death Hook Visibility
-   Problem
-   Rules added
-     1. Boundary failure kills visibility
-     2. Confirmed resolve node required
-     3. Near-Death retracement required
-     4. Arc endpoint is the confirmed Near-Death resolve node
-   New inputs
-   New sequence audit fields
-   Remaining architecture note

## Concepts

- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/01_scope_and_inputs|01 — Scope and Inputs]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/03_sequence_builder|03 — Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10 — Hook Phase 03 Implementation: Y-Axis Opposite Extremes]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|11 — Hook Phase 04 Implementation: ND, Death Lifecycle, and X Closure Skeleton]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
