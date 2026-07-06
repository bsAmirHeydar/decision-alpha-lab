---
title: "11 — Hook Phase 04 Implementation: ND, Death Lifecycle, and X Closure Skeleton"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "2586"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# 11 — Hook Phase 04 Implementation: ND, Death Lifecycle, and X Closure Skeleton

**Source:** [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `2586` bytes

## خلاصه

Phase 04 adds lifecycle diagnostics to the CycleHook architecture: This phase still does not add Hook Type A/B/C. Phase 02 created X sequences. Phase 03 created Y opposite Extremes. Phase 04 uses those objects to create a visible lifecycle skeleton before final type classification and full closure logic. This is still a skeleton. It exposes lifecycle states and thresholds for audit. It does not yet produce a trade signal and does not send orders. Phase 04 treats ND as a return-toward-origin candidate. Given the Phase 02 sequence definitions: The default ND threshold is 50% of the distance from the latest X node back toward origin. Phase 04 draws a death/origin boundary at the origin price. I

## Headings

- 11 — Hook Phase 04 Implementation: ND, Death Lifecycle, and X Closure Skeleton
-   Phase Goal
-   Why This Phase Exists
-   Important Interpretation
-   ND Candidate
-   Death / Origin Return Penetration
-   X Closure Skeleton
-   Lifecycle States
-   Chart Objects
-   CSV Outputs
-   Deferred to Future Phases
-   No Execution Boundary

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10 — Hook Phase 03 Implementation: Y-Axis Opposite Extremes]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14 — NDS Hook Phase 07: Visual Profile Orchestrator]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/nds_hook_architecture/01_scope_and_inputs|01 — Scope and Inputs]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/03_sequence_builder|03 — Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/04_x_y_closure_and_hook_types|04 — X/Y Closure and Hook Types]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
