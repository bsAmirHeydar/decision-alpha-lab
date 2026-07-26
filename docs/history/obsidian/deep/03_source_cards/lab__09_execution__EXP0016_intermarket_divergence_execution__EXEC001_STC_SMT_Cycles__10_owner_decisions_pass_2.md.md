
---
type: source_card
source_path: "docs/evidence/10_owner_decisions_pass_2/19b8476ed547_10_owner_decisions_pass_2.md"
source_ext: ".md"
source_size: 2658
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "UI / React"]
entities: ["EXEC001"]
---

# Source Card — 10_owner_decisions_pass_2.md

## Source

[[docs/evidence/10_owner_decisions_pass_2/19b8476ed547_10_owner_decisions_pass_2|docs/evidence/10_owner_decisions_pass_2/19b8476ed547_10_owner_decisions_pass_2.md]]

## Summary

This document records the second owner clarification pass for EXEC001 STC SMT Cycles. Equality counts as touch. If SL or TP is reached during an M gap, normal position management applies. No new entries or detections occur in gaps. Partial happens exactly at W4 end. Missed partial must be performed later at the first opportunity if the position is still open and not already partialed. Missed partial is performed even if the system is already in a later M. M3 partial can be disabled because hard close dominates. If hard close is missed, it must be performed at the first opportunity. Backtest entry uses the open of the next check candle. Check candles are anchored from 20:00 New York. The final check candle of each M cannot produce entry. If multiple valid references exist, select the reference that produces the largest stop distance on the clean traded symbol. If multiple references exist

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXEC001

## Headings

- 10 - Owner Decisions Pass 2
  - Locked decisions

## Related Source Documents

- [[docs/evidence/00_strategy_document_map/7a03efa653e6_00_strategy_document_map|00_strategy_document_map.md]] — score `12`
- [[docs/evidence/09_owner_decisions_pass_1/d64c20e06d5e_09_owner_decisions_pass_1|09_owner_decisions_pass_1.md]] — score `12`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `12`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `12`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|30_level_09_paper_outcome_simulator.md]] — score `12`
- [[docs/evidence/level_11_paper_hard_close_simulator_15_30_end_day_accounting/d27b26fac569_32_level_11_hard_close_simulator|32_level_11_hard_close_simulator.md]] — score `12`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
