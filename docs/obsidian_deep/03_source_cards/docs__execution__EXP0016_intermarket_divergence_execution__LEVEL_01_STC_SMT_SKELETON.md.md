
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_01_STC_SMT_SKELETON.md"
source_ext: ".md"
source_size: 545
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "MQL Native"]
entities: []
---

# Source Card — LEVEL_01_STC_SMT_SKELETON.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_01_STC_SMT_SKELETON|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_01_STC_SMT_SKELETON.md]]

## Summary

This patch adds the first compileable MQL5 shell for `EXEC001_STC_SMT_Cycles`. The level is deliberately safe: it validates inputs, creates runtime journals, starts a timer, prints locked rules, and prevents duplicate instances. It does not detect signals and it does not trade. Compile target: `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5` Primary documentation: `lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton.md`

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

—

## Headings

- Level 01 — STC SMT Skeleton Patch

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `14`
- [signals.yaml](../../registry/signals.yaml) — score `10`
- [[docs/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|IMPLEMENTATION_PLAN_INDEX.md]] — score `7`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md]] — score `7`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR|LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR.md]] — score `7`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR.md]] — score `7`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `7`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER.md]] — score `7`
- [[docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX|LEGACY_COMPILE_FIX.md]] — score `6`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015_cme_live_backtest_plan.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
