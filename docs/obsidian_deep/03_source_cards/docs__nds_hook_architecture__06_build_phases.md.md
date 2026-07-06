
---
type: source_card
source_path: "docs/nds_hook_architecture/06_build_phases.md"
source_ext: ".md"
source_size: 4242
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Python Brain", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 06_build_phases.md

## Source

[[docs/nds_hook_architecture/06_build_phases|docs/nds_hook_architecture/06_build_phases.md]]

## Summary

Find the central expert that currently performs F-counting / Rally display. Add display-family inputs, but keep default behavior as Rally-only. Acceptance: Build a Hook node adapter from the existing structural nodes used by F-counting. Acceptance: Implement CycleHook objects for positive and negative directions. Acceptance: Implement positive and negative strict sequence building. Acceptance: Extract X nodes and Y opposite Extremes. Acceptance: Implement: Acceptance: Implement positive and negative A/B/C classification. Acceptance: Add display controls for Hook-only, Rally-only, and both. Acceptance: Add optional audit outputs. Acceptance: Run visual smoke tests on: Once the visual and audit behavior is stable, freeze Hook v1. After freeze, Hook can become training input. Acceptance: The current implementation sequence has one additional refinement layer before view finalization: Phase

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- 06 — Build Phases
  - Phase 0 — Locate Central Expert and Protect Rally
  - Phase 1 — Node Source Adapter
  - Phase 2 — CycleHook Object Model
  - Phase 3 — Multi-Sequence Builder
  - Phase 4 — X/Y Extraction
  - Phase 5 — Closure + ND + Death
  - Phase 6 — Hook Type A/B/C
  - Phase 7 — Visualization Controls
  - Phase 8 — Audit and CSV Export
  - Phase 9 — Smoke Test
  - Phase 10 — Freeze Hook v1

## Related Source Documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `22`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `22`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `22`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `21`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `21`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `20`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|answer_normalized_en.md]] — score `20`
- [[docs/experience_capture/answers/EXT-08/notes_en|notes_en.md]] — score `20`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `20`
- [[docs/experience_capture/answers/NDS-R01/notes_en|notes_en.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
