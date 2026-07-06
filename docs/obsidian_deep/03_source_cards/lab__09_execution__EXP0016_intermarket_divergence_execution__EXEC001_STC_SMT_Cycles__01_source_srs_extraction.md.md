
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/01_source_srs_extraction.md"
source_ext: ".md"
source_size: 6464
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "MQL Native", "UI / React"]
entities: []
---

# Source Card — 01_source_srs_extraction.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/01_source_srs_extraction|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/01_source_srs_extraction.md]]

## Summary

This file is a factual English extraction from `STC Expert Advisor SRS.pdf`. It does not add trading assumptions beyond the source. Implementation interpretations and unresolved questions are handled in later files. Expert Advisor name: `STC Expert Advisor`. Purpose: automate the STC strategy based on SMT divergence between two tradable indices. The strategy must only use information from the current trading day. No prior-day information should be used in decision-making after the daily reset. The EA is attached only once, on one chart. The chart symbol does not affect EA logic. All analysis is performed only on two input symbols. All trade management is also limited to those two symbols. STC trading day starts at New York 20:00. STC trading day ends at New York 15:30 the next day. At New York 15:30: all open trades are closed; all strategy states are reset; all counters are reset to zer

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- 01 - Source SRS Extraction
  - 1. Project identity
  - 2. General architecture
  - 3. STC trading day
  - 4. Time management
  - 5. M cycles
  - 6. W cycles
    - M1 W cycles
    - M2 W cycles
    - M3 W cycles
  - 7. Inputs
  - 8. SMT divergence definition

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/08_open_questions|08_open_questions.md]] — score `13`
- [[docs/principles|principles.md]] — score `12`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `12`
- [signals.yaml](../../registry/signals.yaml) — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `9`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
