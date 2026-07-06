
---
type: source_card
source_path: "mql5/Experts/IntermarketDivergence/README.md"
source_ext: ".md"
source_size: 637
empty: false
generated_at: 2026-07-06
concepts: ["Intermarket Divergence", "MQL Native", "Python Brain", "Validation / Audit"]
entities: ["EXP0015"]
---

# Source Card — README.md

## Source

[[mql5/Experts/IntermarketDivergence/README|mql5/Experts/IntermarketDivergence/README.md]]

## Summary

Batch expert for EXP0015. It scans two aligned symbols, usually S&P/US500 and Nasdaq/NAS100, and records time-step divergences between their highs/lows. The expert is intentionally not tick-driven. `OnTick()` is empty. In research mode the whole scan runs once in `OnInit()` and exports CSV files to Common Files. Default output: Turn on `InpWriteAllEvaluatedSteps` only when you need a full audit table for every compared high/low step. It can be large.

## Concepts

[[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0015

## Headings

- Intermarket Divergence Experts
  - IMD001_SPX_NDX_TimeDivergence

## Related Source Documents

- [[docs/EXP0015_cme_live_backtest_plan|EXP0015_cme_live_backtest_plan.md]] — score `13`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|README.md]] — score `13`
- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|README.md]] — score `11`
- [[tools/cme_bridge/README|README.md]] — score `11`
- [[docs/execution/EXP0015_intermarket_time_divergence/LEGACY_COMPILE_FIX|LEGACY_COMPILE_FIX.md]] — score `9`
- [[docs/EXP0015_cme_live_provider_patch|EXP0015_cme_live_provider_patch.md]] — score `9`
- [metadata.yaml](../../lab/03_experiments/EXP0015_intermarket_time_divergence/metadata.yaml) — score `9`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md]] — score `8`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR|LEVEL_11_STC_SMT_HARD_CLOSE_SIMULATOR.md]] — score `8`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
