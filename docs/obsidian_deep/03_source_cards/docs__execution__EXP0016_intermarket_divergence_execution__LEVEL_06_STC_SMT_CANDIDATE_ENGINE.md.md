
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE.md"
source_ext: ".md"
source_size: 732
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "Validation / Audit"]
entities: ["EXEC001"]
---

# Source Card — LEVEL_06_STC_SMT_CANDIDATE_ENGINE.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_06_STC_SMT_CANDIDATE_ENGINE.md]]

## Summary

This document indexes the Level 06 implementation for EXEC001 STC SMT Cycles. Level 06 converts raw touch-only previous-W hunts into audit-only SMT candidate rows. It adds: high-side SMT candidate detection, low-side SMT candidate detection, clean-symbol trade mapping, same-check buy/sell forgetting, largest-stop reference selection using the clean symbol check close as the provisional entry proxy, candidate audit CSV output. It still does not confirm, consume, trade, simulate, draw, partially close, or hard-close positions. Primary detailed document: `docs/evidence/level_06_smt_candidate_engine/97fffdd7f422_27_level_06_smt_candidate_engine.md`

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXEC001

## Headings

- Level 06 STC SMT Candidate Engine

## Related Source Documents

- [[docs/evidence/level_06_smt_candidate_engine/97fffdd7f422_27_level_06_smt_candidate_engine|27_level_06_smt_candidate_engine.md]] — score `16`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR.md]] — score `14`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY.md]] — score `14`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR|LEVEL_09_STC_SMT_PAPER_OUTCOME_SIMULATOR.md]] — score `14`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR.md]] — score `14`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `14`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS|LEVEL_14_STC_SMT_PAPER_LIVE_ALERTS.md]] — score `14`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER|LEVEL_18_STC_SMT_REAL_HARD_CLOSE_FINALIZER.md]] — score `14`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `13`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
