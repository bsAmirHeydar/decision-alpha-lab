
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README.md"
source_ext: ".md"
source_size: 7026
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["EXEC001"]
---

# Source Card — README.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README.md]]

## Summary

This folder contains the locked specification and implementation blueprint for the **STC SMT Cycles** strategy. The strategy is an execution model for two-index SMT divergence. It trades only the two configured symbols, it is independent of the chart symbol, and it must not use information from outside the current STC trading day… The documents in this folder are intentionally layered. The goal is to make the strategy reusable, auditable, and implementable without hiding logic inside one large EA file. Status: **Locked specification, ready for research/paper engine implementation**. The strategy rules have been normalized from the source SRS and then refined through owner clarification passes. The remaining implementation work is no longer conceptual; it is engineering: build the cycle engine, SMT d… `00_strategy_document_map.md` explains how to read the documentation set. `01_source_srs

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

EXEC001

## Headings

- EXEC001 STC SMT Cycles
  - Current status
  - Document map
  - Locked one-line strategy definition
  - Core locked rules
  - Current engineering level: Level 14
  - Level 07 — Confirmation and Signal Registry
  - Level 14 implementation note

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `28`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|35_level_14_paper_live_alerts.md]] — score `26`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/00_strategy_document_map|00_strategy_document_map.md]] — score `24`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|30_level_09_paper_outcome_simulator.md]] — score `24`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/32_level_11_hard_close_simulator|32_level_11_hard_close_simulator.md]] — score `24`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `23`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/09_owner_decisions_pass_1|09_owner_decisions_pass_1.md]] — score `22`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `22`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `22`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers|11_algorithm_layers.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
