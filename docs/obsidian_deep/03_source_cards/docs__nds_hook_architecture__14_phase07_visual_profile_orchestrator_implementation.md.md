
---
type: source_card
source_path: "docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation.md"
source_ext: ".md"
source_size: 6625
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Market Anatomy", "Python Brain", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 14_phase07_visual_profile_orchestrator_implementation.md

## Source

[[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation.md]]

## Summary

Phase 07 adds a central view-control layer for the Hook stack. The previous phases are now structurally independent: That modularity is correct, but it creates a chart-management problem: if all phases draw at the same time, the chart becomes noisy and stale objects from a previous view can remain visible after a profile switch. Phase 07 solves that problem by adding a single **view-profile orchestrator**. It does not build new Hook objects and it does not change the Rally/F-counting logic. It only transforms the already existing Phase 01..Phase 06 configs before those phases run. Phase 07 is still diagnostics and visualization infrastructure only. Forbidden in this phase: The central expert now includes: and loads/applies the Phase 07 profile after Phase 01..Phase 06 configs are loaded, but before the Hook phases execute: Default behavior is intentionally conservative: Therefore the exi

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 14 — NDS Hook Phase 07: Visual Profile Orchestrator
  - Purpose
  - Non-execution boundary
  - New files
  - Central expert integration
  - Inputs
  - View profiles
    - KEEP_INPUTS
    - RAW_NODES
    - SEQUENCE_XY
    - LIFECYCLE
    - TYPE_QUALITY

## Related Source Documents

- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `22`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER|FLAG_COUNTING_LEVEL_19_PHASE2_CLOSED_BAR_TRACKER.md]] — score `22`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `22`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC|FLAG_COUNTING_LEVEL_19_STATE_GATE_DASHBOARD_SPEC.md]] — score `22`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `22`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `21`
- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13_phase06_xy_closure_quality_score_implementation.md]] — score `21`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `21`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `20`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
