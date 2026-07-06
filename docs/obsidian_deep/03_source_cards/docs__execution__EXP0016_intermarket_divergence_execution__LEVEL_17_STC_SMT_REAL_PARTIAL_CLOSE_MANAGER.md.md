
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_17_STC_SMT_REAL_PARTIAL_CLOSE_MANAGER.md"
source_ext: ".md"
source_size: 959
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain"]
entities: ["EXEC001"]
---

# Source Card — LEVEL_17_STC_SMT_REAL_PARTIAL_CLOSE_MANAGER.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_17_STC_SMT_REAL_PARTIAL_CLOSE_MANAGER|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_17_STC_SMT_REAL_PARTIAL_CLOSE_MANAGER.md]]

## Summary

Level 17 adds a magic-only real broker partial close layer for EXEC001 STC SMT Cycles. It is disabled by default and only closes real broker volume when the user explicitly enables real partial close and an allowed runtime mode. Key behavior: scans only `Symbol1` and `Symbol2` positions with matching `InpMagicNumber`; applies real partial close at W4/M end for M1 and M2; disables M3 partial because 15:30 New York hard close has priority; rounds 50% close volume upward to broker step; fully closes tiny positions when rounded partial consumes the full volume; writes marker files to avoid duplicate partial after restart; never manages foreign/manual positions; does not create real entries. Output: `stc_level17_real_partial_actions.csv` Safety defaults: `InpEnableRealPartialClose=false` `InpAllowRealPartialInPaperLive=false` `InpRuntimeMode=STC_MODE_RESEARCH_BACKTEST`

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]

## Entities

EXEC001

## Headings

- LEVEL 17 — STC SMT Real Partial Close Manager

## Related Source Documents

- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR.md]] — score `12`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|LEVEL_06_STC_SMT_CANDIDATE_ENGINE.md]] — score `12`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY.md]] — score `12`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR|LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR.md]] — score `12`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR|LEVEL_10_STC_SMT_PARTIAL_CLOSE_SIMULATOR.md]] — score `12`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR.md]] — score `12`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `12`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS|LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS.md]] — score `12`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/00_strategy_document_map|00_strategy_document_map.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
