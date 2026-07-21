
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/23_level_02_time_engine.md"
source_ext: ".md"
source_size: 4956
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 23_level_02_time_engine.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/23_level_02_time_engine|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/23_level_02_time_engine.md]]

## Summary

Status: implemented in patch `EXP0016_STC_SMT_LEVEL02_TIME_ENGINE`. This level is still a no-trade layer. It does not build W highs/lows, does not detect SMT divergence, does not create signals, and does not send orders. Its only responsibility is to convert the terminal time into the ca… The STC strategy is entirely time-driven. Every later decision depends on the correct New York trading-day classification: Whether the current moment belongs to the STC trading day. Whether the current moment is inside M1, M2, M3, or a no-entry gap. Which W cycle is active. Whether the current check candle is the final check candle of an M, which is not allowed to trigger entry. Whether the 15:30 New York hard-close zone is active. If this layer is wrong, all later SMT and execution logic will be wrong even if the divergence code itself is correct. The runtime starts from broker server time. The user su

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Level 02 — STC Time Engine and Cycle Classifier
  - Why this level exists
  - Canonical time model
  - STC trading day
  - M cycle classification
  - W cycle classification
  - Check-candle anchoring
  - Final check candle rule
  - Audit output
  - Acceptance criteria
  - Next level

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `16`
- [[docs/evidence/16_implementation_checklist/29731b650a84_16_implementation_checklist|16_implementation_checklist.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `13`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|40_level_19_validation_pack.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|41_level_20_operator_manual_deployment_profiles.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `13`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
