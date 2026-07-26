
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan.md"
source_ext: ".md"
source_size: 5152
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 06_mql5_architecture_plan.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan.md]]

## Summary

The implementation must be modular. The STC strategy should not be a single large EA with hidden state. It should be built from reusable modules that can later support other SMT/cycle-divergence strategies. MQL5 experts: `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5` MQL5 include modules: `mql5/Include/IntermarketDivergenceExecution/Core/` `mql5/Include/IntermarketDivergenceExecution/STC/` STC modules: `DAL_STC_Types.mqh` `DAL_STC_Time.mqh` `DAL_STC_Cycles.mqh` `DAL_STC_CheckCandles.mqh` `DAL_STC_WLevels.mqh` `DAL_STC_SMTDetector.mqh` `DAL_STC_Confirmation.mqh` `DAL_STC_ReferenceSelector.mqh` `DAL_STC_Risk.mqh` `DAL_STC_PositionManager.mqh` `DAL_STC_StateJournal.mqh` `DAL_STC_TradeJournal.mqh` `DAL_STC_Renderer.mqh` `DAL_STC_InstanceLock.mqh` Shared core modules should include: Broker symbol info reader. Tick value and volume step utilities. Position lookup b

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 06 - MQL5 Architecture Plan
  - 1. Design goal
  - 2. Proposed folder structure
  - 3. Core modules
  - 4. STC EA responsibilities
  - 5. Scheduler algorithm
  - 6. Time engine
  - 7. Cycle engine
  - 8. Check candle engine
  - 9. SMT detector
  - 10. Confirmation and filter pipeline
  - 11. Risk module

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `18`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `16`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `15`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|41_level_20_operator_manual_deployment_profiles.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `15`
- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector|26_level_05_reference_matrix_hunt_detector.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
