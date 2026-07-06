
---
type: source_card
source_path: "docs/nds_hook_architecture/40_phase28_lifecycle_cleanup_clustered_ids.md"
source_ext: ".md"
source_size: 2509
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Hook"]
entities: []
---

# Source Card — 40_phase28_lifecycle_cleanup_clustered_ids.md

## Source

[[docs/nds_hook_architecture/40_phase28_lifecycle_cleanup_clustered_ids|docs/nds_hook_architecture/40_phase28_lifecycle_cleanup_clustered_ids.md]]

## Summary

Fix two operational issues in the minimal Hook semantic view: stale Hook objects must be removed when the timeframe changes, the chart identity changes, or the expert is reattached; branch-number labels must be readable, stacked deterministically below valleys and above peaks, and carry minimal Hook/branch identity. The expert already had cleanup toggles, but Phase 28 hardens lifecycle cleanup by deleting the generic `DAL_HOOK_` namespace in addition to all configured Hook phase prefixes. This handles stale objects from: timeframe changes; expert remove / reattach; recompilation; parameter changes; older Hook profile prefixes; changed input prefixes. A runtime chart-identity guard was added: If the runtime symbol/period identity changes, the expert cleans all known Hook objects, resets the last-bar cache, redraws the chart, and runs the engine again. Branch-number labels now optionally i

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Hook|Hook]]

## Entities

—

## Headings

- Phase 28 — Lifecycle Cleanup and Clustered Hook/Branch Label IDs
  - Goal
  - Cleanup behavior
  - Label identity
  - Label clustering
  - Vertical placement
  - Rendering order

## Related Source Documents

- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `11`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10_phase03_y_axis_opposite_extremes_implementation.md]] — score `11`
- [[docs/nds_hook_architecture/12_phase05_hook_type_abc_classifier_implementation|12_phase05_hook_type_abc_classifier_implementation.md]] — score `11`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `11`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `10`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `10`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA.md]] — score `10`
- [[docs/debug/E0008/README|README.md]] — score `10`
- [[docs/experience_capture/answers/ENT-R01/notes_en|notes_en.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
