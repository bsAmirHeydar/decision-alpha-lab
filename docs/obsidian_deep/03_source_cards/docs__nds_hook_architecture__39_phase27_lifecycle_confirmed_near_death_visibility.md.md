
---
type: source_card
source_path: "docs/nds_hook_architecture/39_phase27_lifecycle_confirmed_near_death_visibility.md"
source_ext: ".md"
source_size: 2566
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Hook", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 39_phase27_lifecycle_confirmed_near_death_visibility.md

## Source

[[docs/nds_hook_architecture/39_phase27_lifecycle_confirmed_near_death_visibility|docs/nds_hook_architecture/39_phase27_lifecycle_confirmed_near_death_visibility.md]]

## Summary

The Phase 26 rebuild aligned the branch builder with the Hook/ND branch documentation, but the semantic renderer was still too permissive: a Hook could still visually span across its own floor/ceiling boundary; unconfirmed final nodes could still produce visible structure; arcs could be drawn before the last same-side node was confirmed in the Near-Death area; the renderer was still allowed to infer an end point from counted nodes instead of the confirmed lifecycle resolve node. This contradicts the lifecycle rule: > If the Hook floor/ceiling is touched or penetrated, the Hook is failed/dead. > If the final node is confirmed in Near-Death, draw only to that node. > If it is not confirmed, do not draw the Hook in semantic view. For a low-side / positive Hook: For a high-side / negative Hook: When `death_on_boundary_touch` is enabled, equality also kills the Hook. This matches the practica

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phase 27 — Lifecycle-Aligned Confirmed Near-Death Hook Visibility
  - Problem
  - Rules added
    - 1. Boundary failure kills visibility
    - 2. Confirmed resolve node required
    - 3. Near-Death retracement required
    - 4. Arc endpoint is the confirmed Near-Death resolve node
  - New inputs
  - New sequence audit fields
  - Remaining architecture note

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `14`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `14`
- [[docs/nds_hook_architecture/03_sequence_builder|03_sequence_builder.md]] — score `9`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `9`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `9`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10_phase03_y_axis_opposite_extremes_implementation.md]] — score `9`
- [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|11_phase04_nd_death_x_closure_skeleton_implementation.md]] — score `9`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `9`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `9`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `9`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
