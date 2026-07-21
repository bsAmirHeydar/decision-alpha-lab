
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/README.md"
source_ext: ".md"
source_size: 1633
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Licensing", "UI / React", "Validation / Audit"]
entities: ["EXEC001", "EXP0016"]
---

# Source Card — README.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/README|docs/execution/EXP0016_intermarket_divergence_execution/README.md]]

## Summary

This documentation index points to the execution documentation inside the lab folder. Main strategy: `lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/` EXEC001 STC SMT Cycles is documented as a layered executable specification and implemented level by level. Current code level: **Level 14 — Paper Live Alerts**. Level 14 monitors the full paper/audit pipeline and emits no-order alerts for new signal, paper entry, outcome, partial, and hard-close rows. It still sends no real broker orders. Key detailed documents: `17_implementation_plan.md` `18_module_breakdown.md` `19_patch_build_sequence.md` `21_first_patch_scope.md` `22_level_01_skeleton.md` `23_level_02_time_engine.md` `24_level_03_check_candle_aggregator.md` `25_level_04_w_level_builder.md` `26_level_05_reference_matrix_hunt_detector.md` `27_level_06_smt_candidate_engine.md` The next engineering stage

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXEC001, EXP0016

## Headings

- EXP0016 Intermarket Divergence Execution Documentation
  - Level 22 — Hidden Offline License Fix

## Related Source Documents

- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `22`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `21`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `21`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `21`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `21`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `21`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS|LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS.md]] — score `20`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/README|README.md]] — score `18`
- [[docs/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|IMPLEMENTATION_PLAN_INDEX.md]] — score `17`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX|LEVEL_22_STC_SMT_HIDDEN_LICENSE_FIX.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
