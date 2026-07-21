
---
type: source_card
source_path: "docs/evidence/level_11_paper_hard_close_simulator_15_30_end_day_accounting/d27b26fac569_32_level_11_hard_close_simulator.md"
source_ext: ".md"
source_size: 4438
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["EXEC001"]
---

# Source Card — 32_level_11_hard_close_simulator.md

## Source

[[docs/evidence/level_11_paper_hard_close_simulator_15_30_end_day_accounting/d27b26fac569_32_level_11_hard_close_simulator|docs/evidence/level_11_paper_hard_close_simulator_15_30_end_day_accounting/d27b26fac569_32_level_11_hard_close_simulator.md]]

## Summary

Level 11 adds the paper hard-close accounting layer for EXEC001 STC SMT Cycles. It does not place real broker orders and it does not close real positions. Its only purpose is to answer the question: for every paper trade… This level implements the locked owner rule that no STC trade may remain open after 15:30 New York. In the research/paper layer, this means that any paper volume still open at the 15:30 check-candle close is force-closed… Level 11 includes: 15:30 New York hard-close checkpoint detection. Delayed hard-close recovery if the EA was not running exactly at 15:30. Full-volume paper hard close when no partial happened. Remaining-volume paper hard close when W4 partial already reduced the position. No hard close if TP, SL, or ambiguous outcome occurred before 15:30. No hard close if the W4 partial fully consumed a tiny-volume paper trade. Dedicated hard-close audit CSV. Level 1

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXEC001

## Headings

- Level 11 — Paper Hard-Close Simulator and 15:30 End-of-Day Accounting
  - Purpose
  - Scope
  - Locked rules implemented
  - Algorithm
  - Output
  - Acceptance criteria

## Related Source Documents

- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `16`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `16`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/30_level_09_paper_outcome_simulator|30_level_09_paper_outcome_simulator.md]] — score `16`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|35_level_14_paper_live_alerts.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/38_level_17_real_partial_close_manager|38_level_17_real_partial_close_manager.md]] — score `16`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|40_level_19_validation_pack.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
