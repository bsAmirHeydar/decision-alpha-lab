
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/27_level_06_smt_candidate_engine.md"
source_ext: ".md"
source_size: 6096
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Known-Time Causality", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 27_level_06_smt_candidate_engine.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/27_level_06_smt_candidate_engine|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/27_level_06_smt_candidate_engine.md]]

## Summary

Status: implemented as an audit-only layer. Level 06 converts the raw hunt material from Level 05 into explicit SMT candidate rows. It still does not confirm signals, consume signals, simulate entries, open positions, draw objects, or manage trades. The output of… Level 06 is responsible for these operations: Read the closed check-candle context from the Level 03 aggregator. Rebuild the legal previous-W reference set from Level 05. Read raw high/low hunt patterns for every legal reference. Convert exactly-one high hunts into sell-side SMT material. Convert exactly-one low hunts into buy-side SMT material. Discard the entire check candle if buy-side and sell-side SMT material appear in the same check candle. Select the reference that creates the largest provisional stop distance on the clean traded symbol. Emit audit-only SMT candidate rows. Keep all output causal: no next-candle entry pr

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 06 — SMT Candidate Engine
  - Scope
  - Non-scope
  - Candidate conversion rules
    - High-side SMT
    - Low-side SMT
  - Same-check ambiguity rule
  - Reference selection rule
  - Multiple same-direction candidates
  - Candidate identity
  - Output
  - Expected outputs after attach

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk|05_execution_and_risk.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13_data_model_and_journals.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/16_implementation_checklist|16_implementation_checklist.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|19_patch_build_sequence.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
