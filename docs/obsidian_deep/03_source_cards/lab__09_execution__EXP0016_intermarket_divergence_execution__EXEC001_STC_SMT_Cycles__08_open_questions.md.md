
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/08_open_questions.md"
source_ext: ".md"
source_size: 1666
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "Validation / Audit"]
entities: []
---

# Source Card — 08_open_questions.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/08_open_questions|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/08_open_questions.md]]

## Summary

The core strategy is locked. The items below are not blockers for the research/paper implementation. They are optional engineering or research extensions. Whether to expose reference selection as a research input. Canonical default is largest stop distance on the clean traded symbol. Whether to use lower-timeframe path reconstruction for ambiguous SL/TP candles. Canonical default is to mark them `AMBIGUOUS`. Whether to support separate data symbols and execution symbols. Canonical STC uses Symbol1 and Symbol2 as both data and execution symbols. Whether to support broker-specific commission models beyond simple net reporting. Whether to export drawings as screenshots or only render them on chart. Whether to add a calendar for holidays and early closes. Canonical default is no trade when data is missing or incomplete. Whether to add auto-trade mode after research and paper modes are valida

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 08 - Open Questions
  - Optional future knobs
  - No longer open

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `10`
- [[lab/05_validation/VAL001/report|report.md]] — score `10`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `10`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers|11_algorithm_layers.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|19_patch_build_sequence.md]] — score `9`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
