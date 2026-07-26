
---
type: source_card
source_path: "docs/nds_hook_architecture/35_phase25_true_hook_arc_and_extremum_label_stacking.md"
source_ext: ".md"
source_size: 1270
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Hook", "Path Smoothness"]
entities: []
---

# Source Card — 35_phase25_true_hook_arc_and_extremum_label_stacking.md

## Source

[[docs/nds_hook_architecture/35_phase25_true_hook_arc_and_extremum_label_stacking|docs/nds_hook_architecture/35_phase25_true_hook_arc_and_extremum_label_stacking.md]]

## Summary

Fix the remaining mismatch in the minimal Hook view: sequence labels should not overlap labels should stack **below valleys** and **above peaks** the Hook line should be the **Hook envelope arc**, not anything that reads like node-to-node sequence wiring Node-number label placement now uses local point shape instead of Hook direction alone. valley-like nodes -> labels stack below the node peak-like nodes -> labels stack above the node Collision stacking also keys by time, side, and a small price bucket, so close labels on the same swing stack more reliably. The old grouped curve still used a generic smooth curve that could visually resemble a connection overlay. Now the grouped Hook curve is explicitly drawn in two halves: start -> crown crown -> end Both halves are eased curves, and the joint passes exactly through the Hook crown. So the visible line is the Hook envelope itself: start =

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]]

## Entities

—

## Headings

- Phase 25 — True Hook Arc and Extremum-Side Label Stacking
  - Goal
  - What changed
    - 1) Extremum-side label stacking
    - 2) True Hook envelope arc through the Hook crown

## Related Source Documents

- [[docs/nds_hook_architecture/34_phase24_hook_envelope_curve_no_markers|34_phase24_hook_envelope_curve_no_markers.md]] — score `9`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/flag_counting/engineering_pack_v5/01_concepts/CONCEPT_TAXONOMY|CONCEPT_TAXONOMY.md]] — score `8`
- [[docs/flag_counting/engineering_pack_v5/03_explanations/ANTI_PATTERNS_AND_FAILURES|ANTI_PATTERNS_AND_FAILURES.md]] — score `8`
- [[docs/flag_counting/engineering_pack_v5/05_visualization/VISUAL_CONTRACT|VISUAL_CONTRACT.md]] — score `8`
- [[docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT|FLAG_COUNTING_ALGORITHM_BLUEPRINT.md]] — score `8`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2|FLAG_COUNTING_CONCEPT_SPEC_V2.md]] — score `8`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `8`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V3.md]] — score `8`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
