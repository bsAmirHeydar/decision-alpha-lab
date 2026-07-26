
---
type: source_card
source_path: "docs/nds_hook_architecture/34_phase24_hook_envelope_curve_no_markers.md"
source_ext: ".md"
source_size: 1216
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Hook", "Path Smoothness"]
entities: []
---

# Source Card — 34_phase24_hook_envelope_curve_no_markers.md

## Source

[[docs/nds_hook_architecture/34_phase24_hook_envelope_curve_no_markers|docs/nds_hook_architecture/34_phase24_hook_envelope_curve_no_markers.md]]

## Summary

Fix the conceptual mismatch in the minimal Hook rendering: the display should **not** look like nodes being connected the display should show a **single Hook envelope curve** like the user's red semicircle sketch node sequence information should remain visible only through **stacked numbers** all node markers (bold filled circles/arrows) should be removable from the minimal view For each selected Hook-origin group: start = Hook origin crown = opposite-direction Hook extreme across the group's visible X-points positive Hook → highest peak negative Hook → lowest valley end = directional extreme reached **after** the crown positive Hook → lowest valley after the crown negative Hook → highest peak after the crown The rendered curve is a smooth quadratic envelope through `(start, crown, end)`. no straight sequence lines no bold node markers in the minimal profile labels only for visible node

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]]

## Entities

—

## Headings

- Phase 24 — Hook Envelope Curve and Number-Only Sequences
  - Goal
  - Hook envelope semantics
  - Visual behavior

## Related Source Documents

- [[docs/nds_hook_architecture/35_phase25_true_hook_arc_and_extremum_label_stacking|35_phase25_true_hook_arc_and_extremum_label_stacking.md]] — score `9`
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
