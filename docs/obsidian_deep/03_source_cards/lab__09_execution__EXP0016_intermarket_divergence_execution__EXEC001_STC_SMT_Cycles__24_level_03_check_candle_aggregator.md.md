
---
type: source_card
source_path: "docs/evidence/level_03_check_candle_aggregator_pair_data_completeness/dad06b849807_24_level_03_check_candle_aggregator.md"
source_ext: ".md"
source_size: 5744
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 24_level_03_check_candle_aggregator.md

## Source

[[docs/evidence/level_03_check_candle_aggregator_pair_data_completeness/dad06b849807_24_level_03_check_candle_aggregator|docs/evidence/level_03_check_candle_aggregator_pair_data_completeness/dad06b849807_24_level_03_check_candle_aggregator.md]]

## Summary

Level 03 adds the first data layer on top of the Level 02 time engine. The strategy still does not detect SMT, does not construct W reference levels, does not create signals, does not simulate trades, and does not send o… The only job of this level is to convert raw M1 broker data for `Symbol1` and `Symbol2` into deterministic STC check candles aligned from the 20:00 New York STC trading-day anchor. This is the layer that makes later SMT detection safe. If the two-symbol check candle is not complete, no later signal layer is allowed to use it. The following owner decisions are encoded in this level: Check candles are anchored from 20:00 New York. Supported check sizes are 1m, 3m, 5m, 10m, 15m, and 30m. Check candles are internally aggregated from M1 data. Both symbols must have complete data for a check candle to be eligible. Gap periods are no-entry and no-detection zones. No data is in

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Level 03 — Check Candle Aggregator and Pair Data Completeness
  - Purpose
  - Locked owner decisions implemented here
  - Check candle anchoring
  - Aggregation algorithm
  - Completeness rule
  - Active-M and gap behavior
  - Final check behavior
  - Runtime behavior
  - Backfill and catch-up
  - Output file
  - Acceptance criteria

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[docs/evidence/16_implementation_checklist/29731b650a84_16_implementation_checklist|16_implementation_checklist.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/23_level_02_time_engine|23_level_02_time_engine.md]] — score `11`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|40_level_19_validation_pack.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|41_level_20_operator_manual_deployment_profiles.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
