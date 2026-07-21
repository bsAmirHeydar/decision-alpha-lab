
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR.md"
source_ext: ".md"
source_size: 671
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "MQL Native", "Python Brain", "Validation / Audit"]
entities: ["EXEC001"]
---

# Source Card — LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR.md]]

## Summary

Level 11 adds paper-only 15:30 New York hard-close accounting for EXEC001 STC SMT Cycles. It extends Level 10 by adding: a new hard-close audit file, 15:30 New York end-of-day paper close logic, delayed hard-close recovery, remaining-volume close after W4 partial, full-volume close when no partial happened, no real broker orders. The implementation file is: `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_HardClose.mqh` The main EA remains: `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5` Output file: `dal/stc/EXEC001_STC_SMT_Cycles/stc_level11_hard_close_actions.csv`

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXEC001

## Headings

- Level 11 STC SMT Hard Close Simulator

## Related Source Documents

- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `16`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER.md]] — score `16`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `15`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `15`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|35_level_14_paper_live_alerts.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `15`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|README.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
