
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers.md"
source_ext: ".md"
source_size: 5282
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 11_algorithm_layers.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers.md]]

## Summary

This document decomposes the STC strategy into independent algorithms. Inputs: Broker server time. Broker UTC offset input. Optional UTC timestamps from external data. Outputs: New York timestamp. STC trading-day ID. M context. W context. Check-candle context. Hard-close status. Algorithm: Convert all timestamps into UTC. Convert UTC into New York time with DST support. Compute STC trading-day start and end. Reject signal processing outside the active STC day. Assign M, W, gap, and check-candle state. Inputs: Symbol1 bars. Symbol2 bars. Expected interval. Outputs: Complete/incomplete flag. Missing count. Audit reason. Algorithm: For each interval required by the signal engine, load bars for both symbols. Verify both symbols have complete coverage. If either side is incomplete, reject signal logic for that interval. Still write audit output. Inputs: Complete bars for a W interval. Outputs

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- 11 - Algorithm Layers
  - Layer 1: Time normalization
  - Layer 2: Data completeness
  - Layer 3: W builder
  - Layer 4: Reference matrix
  - Layer 5: Hunt detector
  - Layer 6: SMT detector
  - Layer 7: Reference selector
  - Layer 8: Confirmation filter
  - Layer 9: Execution/risk
  - Layer 10: Position management
  - Layer 11: Persistence

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|19_patch_build_sequence.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/15_visualization_contract|15_visualization_contract.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/43_level_21_drawing_audit|43_level_21_drawing_audit.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|40_level_19_validation_pack.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|41_level_20_operator_manual_deployment_profiles.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
