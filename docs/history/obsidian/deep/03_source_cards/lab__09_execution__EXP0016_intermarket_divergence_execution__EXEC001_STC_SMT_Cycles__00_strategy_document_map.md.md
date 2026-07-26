
---
type: source_card
source_path: "docs/evidence/00_strategy_document_map/7a03efa653e6_00_strategy_document_map.md"
source_ext: ".md"
source_size: 2349
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React"]
entities: ["EXEC001"]
---

# Source Card — 00_strategy_document_map.md

## Source

[[docs/evidence/00_strategy_document_map/7a03efa653e6_00_strategy_document_map|docs/evidence/00_strategy_document_map/7a03efa653e6_00_strategy_document_map.md]]

## Summary

This document explains the documentation layers for EXEC001 STC SMT Cycles. STC is not only a signal rule. It is a full execution model that combines time, cycles, two-symbol SMT, confirmation candles, risk sizing, partial management, hard close, restart recovery, and duplicate-instance safety. A single README would become ambiguous. Therefore the strategy is split into layers: Source traceability. Normalized strategy rules. Time and cycle model. SMT divergence model. Execution and risk model. Engineering architecture. Test plan. Persistence and journals. Visualization. Implementation checklist. Each layer should be implementable and testable by itself. Start with `02_normalized_strategy_spec.md` to understand the full strategy. Then read `03_cycle_calendar.md` and `04_smt_divergence_rules.md` because most logic errors will happen in time and divergence detection. Then… The implementatio

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXEC001

## Headings

- 00 - Strategy Document Map
  - Why this strategy is documented in layers
  - Reading order
  - Source hierarchy
  - What is locked
  - What can still be configured as research knobs

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `24`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|README.md]] — score `19`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|README.md]] — score `19`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/README|README.md]] — score `19`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/README|README.md]] — score `17`
- [[docs/evidence/11_algorithm_layers/07355f60fef2_11_algorithm_layers|11_algorithm_layers.md]] — score `17`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `17`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05_execution_and_risk.md]] — score `17`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13_data_model_and_journals.md]] — score `17`
- [[docs/evidence/16_implementation_checklist/29731b650a84_16_implementation_checklist|16_implementation_checklist.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
