
---
type: source_card
source_path: "docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation.md"
source_ext: ".md"
source_size: 6226
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Market Anatomy", "Python Brain", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 17_phase10_freeze_training_contract_implementation.md

## Source

[[docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation|docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation.md]]

## Summary

Phase 10 is the final modular Hook phase for the current NDS architecture pass. It does **not** create a new Hook signal. It freezes the runtime contract that makes Hook output safe to use as downstream training input. The rule is: This phase is a gate, not a strategy. The central expert now exposes the display-family selector as the **first visible input**: Available values: Expected behavior: The default remains `RALLY_ONLY` to preserve old behavior. Documentation overlay: `FP_HookPhase10Visual.mqh` intentionally does not draw Hook structure. Reason: All Phase 10 artifacts are CSV/log contracts. Use when inspecting the contract without asserting readiness. Default. Runs the contract checks but does not imply permanent lock. Use when preparing Hook output for downstream training datasets. Requires clean audit, clean smoke, visible Hook display family, Hook records, quality records, and

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phase 10 — Hook v1 Freeze + Training Contract
  - Purpose
  - First input requirement
  - Added files
  - Phase 10 is no-draw
  - Freeze modes
    - OBSERVE_ONLY
    - V1_CANDIDATE
    - TRAINING_READY
    - STRICT_LOCK
  - Main inputs
  - Contract checks

## Related Source Documents

- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES|FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `20`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `19`
- [[docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation|16_phase09_visual_smoke_test_harness_implementation.md]] — score `19`
- [[docs/nds_hook_architecture/README|README.md]] — score `19`
- [[docs/nds_hook_architecture/14_phase07_visual_profile_orchestrator_implementation|14_phase07_visual_profile_orchestrator_implementation.md]] — score `19`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `18`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
