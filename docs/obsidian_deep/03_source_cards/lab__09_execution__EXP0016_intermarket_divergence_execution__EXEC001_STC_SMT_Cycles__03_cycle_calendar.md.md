
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar.md"
source_ext: ".md"
source_size: 4471
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 03_cycle_calendar.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar.md]]

## Summary

All strategy times are defined in New York time. The implementation must support New York DST. Broker time must be converted into New York time through a broker-to-UTC offset and a New-York DST conversion layer. For external CME or CSV data, the preferred storage time is UTC. The strategy layer converts UTC to New York time for cycle assignment. The STC trading day starts at 20:00 New York and ends at 15:30 New York the following calendar day. The trading-day label is the date of the 15:30 hard close. For example, the STC day that starts Monday 20:00 and ends Tuesday 15:30 is Tuesday's STC trading day. No strategy decision may use candles before the start of the current STC trading day. At 15:30 New York: All open STC positions must be hard-closed. All active divergences are cleared. All cycle states are reset. All trade counters are reset. All partial state flags are reset for the next

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 03 - Cycle Calendar and Time Model
  - 1. Time authority
  - 2. STC trading day
  - 3. Daily reset
  - 4. M cycles
  - 5. No-entry gaps
  - 6. W cycles
  - 7. W high and low construction
  - 8. Check candle anchoring
  - 9. Last check candle rule
  - 10. Cycle assignment algorithm
  - 11. Data completeness algorithm

## Related Source Documents

- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/29_level_08_risk_plan_paper_entry|29_level_08_risk_plan_paper_entry.md]] — score `13`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `13`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `12`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015_cme_live_backtest_plan.md]] — score `12`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `12`
- [[docs/evidence/11_algorithm_layers/07355f60fef2_11_algorithm_layers|11_algorithm_layers.md]] — score `11`
- [[docs/evidence/15_visualization_contract/0ccec648c2ec_15_visualization_contract|15_visualization_contract.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/43_level_21_drawing_audit|43_level_21_drawing_audit.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
