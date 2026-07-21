
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER.md"
source_ext: ".md"
source_size: 676
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "MQL Native", "Python Brain", "Validation / Audit"]
entities: ["EXEC001"]
---

# Source Card — LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER.md]]

## Summary

Patch scope: add the final real broker hard-close layer for EXEC001 STC SMT Cycles. This level is disabled by default. When explicitly enabled, it retries closing only Symbol1/Symbol2 positions with the configured STC magic number after 15:30 New York. It audits every attempt and verifies whether positi… Main implementation file: `mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_RealHardClose.mqh` Main EA: `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5` Primary output: `dal/stc/EXEC001_STC_SMT_Cycles/stc_level18_real_hard_close_finalizer.csv`

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXEC001

## Headings

- LEVEL 18 — STC SMT Real Hard Close Finalizer

## Related Source Documents

- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR.md]] — score `16`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `16`
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
