
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_15_STC_SMT_BROKER_POSITION_MANAGER.md"
source_ext: ".md"
source_size: 561
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "Validation / Audit"]
entities: []
---

# Source Card — LEVEL_15_STC_SMT_BROKER_POSITION_MANAGER.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_15_STC_SMT_BROKER_POSITION_MANAGER|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_15_STC_SMT_BROKER_POSITION_MANAGER.md]]

## Summary

This level adds a magic-only broker position safety layer for `EXEC001_STC_SMT_Cycles`. It does not enable auto-entry. It only scans real broker positions, audits exposure, detects foreign positions on the configured pair, and optionally hard-closes matching magic-number positions after 15:30 New York when… Project-local details are documented in: `lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/36_level_15_broker_position_manager.md`

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 15 — STC SMT Broker Position Manager

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/36_level_15_broker_position_manager|36_level_15_broker_position_manager.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `8`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/08_open_questions|08_open_questions.md]] — score `8`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers|11_algorithm_layers.md]] — score `8`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `8`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `8`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|19_patch_build_sequence.md]] — score `8`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `8`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/26_level_05_reference_matrix_hunt_detector|26_level_05_reference_matrix_hunt_detector.md]] — score `8`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/39_level_18_real_hard_close_finalizer|39_level_18_real_hard_close_finalizer.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
