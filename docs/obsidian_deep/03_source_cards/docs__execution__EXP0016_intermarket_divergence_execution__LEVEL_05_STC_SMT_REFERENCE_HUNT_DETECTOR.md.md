
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md"
source_ext: ".md"
source_size: 1743
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md]]

## Summary

Level 05 adds the previous-W reference matrix and raw touch-only hunt detector for `EXEC001_STC_SMT_Cycles`. It is still an audit-only level. It creates no SMT candidate, no confirmation, no signal, no paper trade, and no live order. EA: `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5` New module: `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Hunts.mqh` Updated modules: `DAL_STC_Enums.mqh` `DAL_STC_Types.mqh` `DAL_STC_Config.mqh` `DAL_STC_Utils.mqh` `DAL_STC_Journal.mqh` `DAL_STC_Engine.mqh` Strategy documentation: `lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector.md` Common Files output: `dal/stc/EXEC001_STC_SMT_Cycles/stc_level05_build_sanity.csv` `dal/stc/EXEC001_STC_SMT_Cycles/stc_level05_runtime_events.csv` `dal/stc/EXEC001_STC_SMT_Cycles/stc_level05_time_audit.csv` `dal/

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 05 — STC SMT Reference Matrix and Raw Hunt Detector
  - Files
  - Output
  - Runtime inputs added
  - Locked behavior

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector|26_level_05_reference_matrix_hunt_detector.md]] — score `18`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `13`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015_cme_live_backtest_plan.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
