
---
type: source_card
source_path: "docs/evidence/09_owner_decisions_pass_1/d64c20e06d5e_09_owner_decisions_pass_1.md"
source_ext: ".md"
source_size: 2754
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "UI / React", "Validation / Audit"]
entities: ["EXEC001"]
---

# Source Card — 09_owner_decisions_pass_1.md

## Source

[[docs/evidence/09_owner_decisions_pass_1/d64c20e06d5e_09_owner_decisions_pass_1|docs/evidence/09_owner_decisions_pass_1/d64c20e06d5e_09_owner_decisions_pass_1.md]]

## Summary

This document records the first owner clarification pass for EXEC001 STC SMT Cycles. No entries are allowed in the temporal gaps between M cycles. Gap data is not required for signal detection, but open positions must still be managed if final TP or SL is reached. W high and W low are the high and low of a synthetic 90-minute candle. The timeframe used to build them does not change the final high/low if data is complete. W2 can compare only with W1. W3 can compare only with W2 and W1. W4 can compare only with W3, W2, and W1. No W compares with itself. W1 gives no signal. Hunts use no tolerance. Buy and sell side mapping from SMT was confirmed. Each symbol has its own W levels. The comparison is structural, not shared-price. If the clean symbol also hunts before check-candle close, the divergence disappears and no entry is allowed. The close of the same check candle is enough for confirma

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXEC001

## Headings

- 09 - Owner Decisions Pass 1
  - Locked decisions

## Related Source Documents

- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `14`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `14`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|30_level_09_paper_outcome_simulator.md]] — score `14`
- [[docs/evidence/level_11_paper_hard_close_simulator_15_30_end_day_accounting/d27b26fac569_32_level_11_hard_close_simulator|32_level_11_hard_close_simulator.md]] — score `14`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|35_level_14_paper_live_alerts.md]] — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/38_level_17_real_partial_close_manager|38_level_17_real_partial_close_manager.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
