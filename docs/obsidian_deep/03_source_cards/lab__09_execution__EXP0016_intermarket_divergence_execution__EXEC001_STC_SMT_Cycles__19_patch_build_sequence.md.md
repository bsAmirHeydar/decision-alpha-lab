
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence.md"
source_ext: ".md"
source_size: 5864
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["EXEC001"]
---

# Source Card — 19_patch_build_sequence.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence.md]]

## Summary

This document defines the exact engineering sequence for implementation patches. The purpose is to keep each patch small enough to compile, inspect, and debug. Create the EA shell and core types. EA file config structs enums inputs build sanity logs output folder creation timer loop no-op engine signal detection W logic order execution chart drawing beyond optional build label compiles with zero errors can attach to any chart prints all inputs confirms Symbol1 and Symbol2 exist Correctly classify New York time into STC day, M, W, gap, and hard-close zones. time conversion New York DST handling STC day object M/W schedule gap classifier final check candle classifier hard close classifier logs current NY time logs active STC day logs active M/W/gap state test timestamps map correctly Build internal check candles from M1 data. M1 series fetch for both symbols synthetic check candle construc

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

EXEC001

## Headings

- EXEC001 STC SMT Cycles — Patch Build Sequence
  - Patch 001 — EA Skeleton, Inputs, and Build Sanity
    - Goal
    - Adds
    - Must Not Add
    - Acceptance
  - Patch 002 — Time and Cycle Engine
    - Goal
    - Adds
    - Acceptance
  - Patch 003 — Check Candle Aggregator
    - Goal

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `20`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `20`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `20`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `20`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|40_level_19_validation_pack.md]] — score `20`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `20`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `19`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/00_strategy_document_map|00_strategy_document_map.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|30_level_09_paper_outcome_simulator.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
