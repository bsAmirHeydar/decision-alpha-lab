
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/16_implementation_checklist.md"
source_ext: ".md"
source_size: 3882
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 16_implementation_checklist.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/16_implementation_checklist|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/16_implementation_checklist.md]]

## Summary

Confirm documentation is applied. Add deterministic synthetic data fixtures. Add expected output CSV samples. Create types for: STC day. M cycle. W cycle. Check candle. W reference. SMT candidate. Signal intent. Trade plan. Position action. Journal row. Implement: New York conversion. STC day ID. M assignment. W assignment. Gap detection. Check-candle anchoring from 20:00. Final check candle detection. Hard-close time detection. Implement: Symbol1/Symbol2 data loader. Check-candle aggregator. W high/low builder. Completeness detector. Current-day data restriction. Implement: W reference matrix. Touch-only hunt detector. High/low SMT candidate builder. Clean/hunted symbol selector. Side mapper. Largest-stop reference selector. Implement: Check-candle close confirmation. Clean symbol late hunt invalidation. Final check candle expiration. Buy/sell ambiguity discard. Duplicate consumed signa

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- 16 - Implementation Checklist
  - Phase 0: Documentation and test fixtures
  - Phase 1: Core types
  - Phase 2: Time and cycle engine
  - Phase 3: Data and aggregation
  - Phase 4: SMT detector
  - Phase 5: Confirmation and filtering
  - Phase 6: Risk and trade planning
  - Phase 7: Research backtest
  - Phase 8: Journals and restart persistence
  - Phase 9: Drawing
  - Phase 10: Paper live

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `16`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `16`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|19_patch_build_sequence.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/23_level_02_time_engine|23_level_02_time_engine.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|40_level_19_validation_pack.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|41_level_20_operator_manual_deployment_profiles.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
