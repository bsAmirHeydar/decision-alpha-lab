
---
type: source_card
source_path: "docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation.md"
source_ext: ".md"
source_size: 2393
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 09_phase02_cyclehook_sequence_builder_implementation.md

## Source

[[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation.md]]

## Summary

Phase 02 turns the Phase 01 peak/valley node stream into actual CycleHook sequence candidates. This is still not the full Hook engine. Phase 02 builds: It does not yet build: Those come in later phases. The central expert receives a second Hook module: Phase 02 uses the Phase 01 node source adapter internally and respects the same display family: Default remains Rally-only, so existing F-counting behavior is preserved. A positive Hook sequence starts from a valley and accepts strictly lower valley nodes. Equal lows are rejected because the strict node source and strict sequence rule do not accept equality. A negative Hook sequence starts from a peak and accepts strictly higher peak nodes. Equal highs are rejected. Phase 02 draws the death boundary at the origin price. This is only a structural boundary marker in Phase 02. Full death/ND lifecycle is intentionally deferred to a later phase

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder
  - Phase Goal
  - Integration Contract
  - Positive CycleHook Sequence
  - Negative CycleHook Sequence
  - Origin and Death Boundary
  - Sequence States
  - Display Objects
  - CSV Outputs
  - No Execution Boundary

## Related Source Documents

- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `21`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `21`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `21`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
