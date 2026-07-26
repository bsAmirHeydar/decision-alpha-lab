
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_16_STC_SMT_REAL_AUTO_ENTRY_ROUTER.md"
source_ext: ".md"
source_size: 374
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence"]
entities: []
---

# Source Card — LEVEL_16_STC_SMT_REAL_AUTO_ENTRY_ROUTER.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_16_STC_SMT_REAL_AUTO_ENTRY_ROUTER|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_16_STC_SMT_REAL_AUTO_ENTRY_ROUTER.md]]

## Summary

Patch scope: gated real market entry from confirmed STC paper plans. Main document: `lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/37_level_16_real_auto_entry_router.md` Default safety: real auto-entry is disabled. Enable only with `STC_MODE_AUTO_TRADE` and `InpEnableRealAutoEntry=true`.

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]]

## Entities

—

## Headings

- Level 16 — STC SMT Real Auto Entry Router

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/37_level_16_real_auto_entry_router|37_level_16_real_auto_entry_router.md]] — score `12`
- [[docs/execution/EXP0016_intermarket_divergence_execution/IMPLEMENTATION_PLAN_INDEX|IMPLEMENTATION_PLAN_INDEX.md]] — score `5`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_01_STC_SMT_SKELETON|LEVEL_01_STC_SMT_SKELETON.md]] — score `5`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] — score `5`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR.md]] — score `5`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER|LEVEL_04_STC_SMT_W_LEVEL_BUILDER.md]] — score `5`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md]] — score `5`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|LEVEL_06_STC_SMT_CANDIDATE_ENGINE.md]] — score `5`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY|LEVEL_07_STC_SMT_CONFIRMATION_SIGNAL_REGISTRY.md]] — score `5`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY.md]] — score `5`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
