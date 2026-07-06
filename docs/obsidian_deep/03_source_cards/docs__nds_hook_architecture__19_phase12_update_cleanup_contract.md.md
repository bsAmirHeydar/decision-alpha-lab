
---
type: source_card
source_path: "docs/nds_hook_architecture/19_phase12_update_cleanup_contract.md"
source_ext: ".md"
source_size: 1620
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Hook", "Validation / Audit"]
entities: []
---

# Source Card — 19_phase12_update_cleanup_contract.md

## Source

[[docs/nds_hook_architecture/19_phase12_update_cleanup_contract|docs/nds_hook_architecture/19_phase12_update_cleanup_contract.md]]

## Summary

When the expert updates, the previous Hook drawings must not remain on the chart. The chart must represent the current calculation pass only. Phase 07 cleanup is now extended from P01..P07 to the full Hook overlay namespace P01..P10. A common prefix cleanup was also added: `InpHookPhase07CleanCommonHookPrefix` `InpHookPhase07CommonHookObjectPrefix = "DAL_HOOK_"` This deletes stale objects from older Hook phases or previous prefixes before the current pass redraws. New cleanup toggles: `InpHookPhase07CleanP08Objects` `InpHookPhase07CleanP09Objects` `InpHookPhase07CleanP10Objects` All are enabled by default. Phase 07 now also stores the cleanup prefixes for: Phase 08 audit objects / future objects Phase 09 smoke-test panel objects Phase 10 freeze / contract objects On each update pass, before the Hook phases draw again: Phase 07 deletes existing Hook objects by the common `DAL_HOOK_` prefi

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- NDS Hook Phase 12 — Update Cleanup Contract
  - Purpose
  - Change
  - Runtime behavior
  - Default

## Related Source Documents

- [[docs/nds_hook_architecture/01_scope_and_inputs|01_scope_and_inputs.md]] — score `7`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `7`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08_phase01_node_source_adapter_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/10_phase03_y_axis_opposite_extremes_implementation|10_phase03_y_axis_opposite_extremes_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/11_phase04_nd_death_x_closure_skeleton_implementation|11_phase04_nd_death_x_closure_skeleton_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `7`
- [[docs/nds_hook_architecture/37_phase26_doc_aligned_hook_rebuild|37_phase26_doc_aligned_hook_rebuild.md]] — score `7`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
