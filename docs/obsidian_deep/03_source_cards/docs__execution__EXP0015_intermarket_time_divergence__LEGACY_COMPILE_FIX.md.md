
---
type: source_card
source_path: "docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX.md"
source_ext: ".md"
source_size: 1908
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Intermarket Divergence", "MQL Native"]
entities: ["EXP0015"]
---

# Source Card — LEGACY_COMPILE_FIX.md

## Source

[[docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX|docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX.md]]

## Summary

This patch fixes compile errors triggered by the deprecated expert: `mql5/Experts/IntermarketDivergence/IMD001_SPX_NDX_TimeDivergence.mq5` `mql5/Include/IntermarketDivergence/DAL_IMDReferenceLevels.mqh` The project had two EXP0015 API generations mixed together: The current simple candle/session engine uses `IMD_*` types: `IMD_LevelFamily` `IMD_TriggerMode` `IMD_Event` The deprecated SPX/NDX expert and old reference-level module used older `DAL_IMD*` names: `DAL_IMDLevelSide` `DAL_IMDLevelSource` `DAL_IMDTriggerMode` `DAL_IMDReferenceLevel` MetaEditor therefore reported errors such as `declaration without type`, `side - comma expected`, and undeclared `IMD_LEVEL_HIGH` or `IMD_LEVEL_L_NODE`. Adds compile-compatible aliases and compatibility structs in `DAL_IMDTypes.mqh`. Extends `IMD_LevelFamily` with legacy node/day enum values so older inputs compile. Keeps the simple EXP0015 engine det

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

EXP0015

## Headings

- EXP0015 Legacy Compile Fix
  - Cause
  - What the fix does
  - Recommended compile target
  - Important limitation

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `12`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `12`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015_cme_live_backtest_plan.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|README.md]] — score `11`
- [[tools/cme_bridge/README|README.md]] — score `11`
- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|README.md]] — score `9`
- [[mql5/Experts/IntermarketDivergence/README|README.md]] — score `9`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
