
---
type: source_card
source_path: "docs/evidence/level_10_paper_partial_close_simulator_w4_management/91dce4903990_31_level_10_partial_close_simulator.md"
source_ext: ".md"
source_size: 3233
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 31_level_10_partial_close_simulator.md

## Source

[[docs/evidence/level_10_paper_partial_close_simulator_w4_management/91dce4903990_31_level_10_partial_close_simulator|docs/evidence/level_10_paper_partial_close_simulator_w4_management/91dce4903990_31_level_10_partial_close_simulator.md]]

## Summary

Level 10 adds the first paper position-management layer after the Level 09 paper outcome simulator. It does not place real orders, does not modify broker positions, and does not perform hard-close accounting yet. Its only new responsibility is to decide what would happen at the end of W4 for open paper trades. The locked STC rule is: If Partial is OFF, no partial action is taken. If Partial is ON, at the end of W4 of the same M, every trade opened in that M is checked. If the trade has already reached TP, SL, or an ambiguous SL/TP state before or at the W4 checkpoint, no partial action is taken. If the trade is still open at the W4 checkpoint, about 50% of the volume is closed. The 50% close volume is rounded upward to the broker volume step. If rounding consumes the whole position, the paper action is a full close by small volume. M3 partial is disabled because the M3 W4 endpoint is als

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 10 — Paper Partial Close Simulator and W4 Management
  - Scope
  - Inputs added
  - New output
  - Algorithm
  - Examples
  - What is still deferred

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `11`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05_execution_and_risk.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13_data_model_and_journals.md]] — score `11`
- [[docs/evidence/16_implementation_checklist/29731b650a84_16_implementation_checklist|16_implementation_checklist.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
