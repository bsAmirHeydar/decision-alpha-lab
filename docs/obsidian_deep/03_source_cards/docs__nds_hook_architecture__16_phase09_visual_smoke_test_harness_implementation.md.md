
---
type: source_card
source_path: "docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation.md"
source_ext: ".md"
source_size: 5937
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "Rally", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 16_phase09_visual_smoke_test_harness_implementation.md

## Source

[[docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation|docs/nds_hook_architecture/16_phase09_visual_smoke_test_harness_implementation.md]]

## Summary

Phase 09 is the visual smoke-test harness for the NDS Hook stack. It does not create a new Hook signal, does not classify trade direction, and does not execute orders. Its only purpose is to verify that the selected Phase 07 view profile is visually coherent after Phase 01 through Phase 08 have run. The core question is: Phase 09 is therefore a post-run inspector. It consumes the configs and runtime reports of the previous phases. It does not rebuild sequences and it does not mutate Phase 01 through Phase 08 logic. Phase 09 is included in: Runtime order: Phase 07 is still applied before the Hook phases run because it transforms the visual configs for Phase 01 through Phase 06. Default behavior is conservative: Therefore existing Rally/F-counting behavior remains unchanged by default. If enabled, Phase 09 requires Phase 08 to be OK. This prevents a clean-looking chart from being trusted w

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phase 09 — Visual Smoke Test Harness Implementation
  - Purpose
  - Position in the Hook stack
  - New modules
  - Central expert integration
  - Inputs
  - Checks
    - 1. Phase 08 audit dependency
    - 2. Object census by Hook prefix
    - 3. Current profile coverage
    - 4. Draw contract when records exist
    - 5. Audit-only no-draw contract

## Related Source Documents

- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15_phase08_audit_csv_reconciliation_implementation.md]] — score `21`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES|FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES.md]] — score `20`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `20`
- [[docs/nds_hook_architecture/06_build_phases|06_build_phases.md]] — score `19`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07_mql5_integration_contract.md]] — score `19`
- [[docs/nds_hook_architecture/17_phase10_freeze_training_contract_implementation|17_phase10_freeze_training_contract_implementation.md]] — score `19`
- [[docs/nds_hook_architecture/README|README.md]] — score `19`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09_phase02_cyclehook_sequence_builder_implementation.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
