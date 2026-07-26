
---
type: source_card
source_path: "lab/03_experiments/EXP0005_mql_native_directional_memory/README.md"
source_ext: ".md"
source_size: 1313
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "MQL Native", "UI / React", "Validation / Audit"]
entities: ["EXP0005", "H0005", "M0005"]
---

# Source Card — README.md

## Source

[[lab/03_experiments/EXP0005_mql_native_directional_memory/README|lab/03_experiments/EXP0005_mql_native_directional_memory/README.md]]

## Summary

Run `M0005_DirectionalMemory.mq5` in MetaTrader Strategy Tester. Expected build sanity line: Key checks: `DAL_M0005_FINAL_OUTCOME_REVERSAL` — structural target success for reversal paths. `DAL_M0005_FINAL_OUTCOME_CONTINUATION` — continuation follow-through before regime change. `DAL_M0005_FINAL_EXCURSION_*` — MFE/MAE until path exit. `DAL_M0005_FINAL_REALIZED_R_*` — realized win rate, R:R, profit factor, and expectancy R. `DAL_M0005_FINAL_FLOATING_R_*` — floating MFE/MAE R, floating R:R, and R-based first-hit order. `DAL_M0005_FINAL_RANDOM_PERFORMANCE_*` — actual versus matched-random win rate, profit factor, expectancy R, MFE R, and floating R:R. `DAL_M0005_FINAL_STRESS_*` — direction-flip and matched-random excursion comparisons. Run multiple regime sources and compare `LAST_ONLY` vs `EWMA_CONTEXT` vs `EWMA_CONSENSUS`. M0005 v1.03 adds `DAL_M0005_FINAL_REVERSAL_TRADE_R1` and `DAL_M0005

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0005, H0005, M0005

## Headings

- EXP0005 — MQL-native H0005 directional memory

## Related Source Documents

- [[docs/mql_native/H0005_DIRECTIONAL_MEMORY|H0005_DIRECTIONAL_MEMORY.md]] — score `24`
- [[lab/02_hypotheses/H0005_directional_memory|H0005_directional_memory.md]] — score `19`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `16`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `14`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `14`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `13`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `13`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `13`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `13`
- [[lab/09_execution/mql5/README|README.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
