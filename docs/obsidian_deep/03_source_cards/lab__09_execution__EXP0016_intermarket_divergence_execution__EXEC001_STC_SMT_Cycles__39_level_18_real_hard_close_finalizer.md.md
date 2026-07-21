
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer.md"
source_ext: ".md"
source_size: 5321
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 39_level_18_real_hard_close_finalizer.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer.md]]

## Summary

Level 18 turns the 15:30 New York hard-close rule into a dedicated real broker finalizer. It does not change the STC signal logic, SMT detection, reference selection, paper simulator, real auto-entry router, or real partial close manager. Its only job is to make sure that, after the STC trading day ends, no remaining real broker position owned by this strategy instance is left open. The finalizer is magic-only. It manages only positions whose symbol is Symbol1 or Symbol2 and whose magic number equals the configured STC magic number. Manual positions, foreign-magic positions, and non-pair symbols are never closed by this module. The STC SRS requires all open STC trades to be closed at 15:30 New York, without exception. The owner clarified that if the hard close was missed because the EA was offline, the hard close must be performed at the first… Level 18 implements that as a retrying brok

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 18 — Real Hard Close Finalizer
  - Purpose
  - Locked Strategy Rule Covered
  - Safety Defaults
  - Position Eligibility
  - Retry Model
  - Verification After Close Attempt
  - Audit Output
  - Relationship to Prior Layers
  - What Level 18 Still Does Not Do
  - Acceptance Criteria

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector|26_level_05_reference_matrix_hunt_detector.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|40_level_19_validation_pack.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|41_level_20_operator_manual_deployment_profiles.md]] — score `13`
- [[docs/evidence/level_20_deployment_profile_matrix/97ecd654ebb6_42_level_20_profile_matrix|42_level_20_profile_matrix.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
