
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/36_level_15_broker_position_manager.md"
source_ext: ".md"
source_size: 5662
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "Python Brain", "Validation / Audit"]
entities: []
---

# Source Card — 36_level_15_broker_position_manager.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/36_level_15_broker_position_manager|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/36_level_15_broker_position_manager.md]]

## Summary

Level 15 is the first layer that looks at the real broker account. It does **not** create entries. It does **not** create market orders for STC signals. It does **not** convert the paper entry model into live trading. Its purpose is narrower and safer: scan real open broker positions, identify only positions belonging to this STC strategy instance, audit those positions into CSV, detect foreign positions on Symbol1/Symbol2, optionally send hard-close orders only for matching magic-number positions after 15:30 New York. Auto-entry remains disabled in this level. The broker manager is allowed to manage only positions where all of the following are true: the position symbol is exactly `Symbol1` or `Symbol2`, the position magic number equals `InpMagicNumber`, the strategy instance lock belongs to this same symbol pair and magic number, hard close is due after 15:30 New York, real hard close

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 15 — Broker Position Manager / Magic-Only Safety Layer
  - Status
  - Locked safety contract
  - Inputs
    - `InpEnableBrokerPositionManager`
    - `InpWriteBrokerPositionAudit`
    - `InpBrokerPositionScanSeconds`
    - `InpEnableRealHardClose`
    - `InpAllowRealCloseInPaperLive`
    - `InpBrokerCloseDeviationPoints`
    - `InpAuditForeignPairPositions`
  - Runtime behavior

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector|26_level_05_reference_matrix_hunt_detector.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer|39_level_18_real_hard_close_finalizer.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|40_level_19_validation_pack.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|41_level_20_operator_manual_deployment_profiles.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
