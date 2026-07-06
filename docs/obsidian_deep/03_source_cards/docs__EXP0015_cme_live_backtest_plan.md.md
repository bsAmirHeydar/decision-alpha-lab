
---
type: source_card
source_path: "docs/EXP0015_cme_live_backtest_plan.md"
source_ext: ".md"
source_size: 1747
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Execution / Risk", "Intermarket Divergence", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["EXP0015"]
---

# Source Card — EXP0015_cme_live_backtest_plan.md

## Source

[[docs/EXP0015_cme_live_backtest_plan|docs/EXP0015_cme_live_backtest_plan.md]]

## Summary

The project now separates the divergence engine from data acquisition. Implemented in this patch: MQL5 candle/session divergence engine. Python backtest runner. Broker data source mode. External CSV data source mode. Session reference levels. Candle reference levels. Step/lag/valid-window logic. Basic MFE/MAE/return outcome columns. Implemented as a stable bridge boundary: `tools/cme_bridge/dal_cme_bridge.py` `serve` mode for localhost HTTP bars. `live_csv_tail` mode for MT5 Common Files. The bridge accepts legally obtained CME or CME-sourced data and normalizes it into DAL candle CSVs. Direct CME/vendor adapters should be added inside this bridge, not inside MQL5. To activate direct CME/vendor live data, provide the credentialed feed details and schema, then implement an adapter that outputs: Expected raw inputs can be: historical bar exports, historical tick/trade exports converted by

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXP0015

## Headings

- EXP0015 CME/live/backtest implementation plan
  - Stage 1: source-agnostic divergence engine
  - Stage 2: live data bridge
  - Stage 3: direct CME/vendor adapter
  - Stage 4: live MQL5 monitor
  - Stage 5: next upgrades

## Related Source Documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|README.md]] — score `15`
- [[tools/cme_bridge/README|README.md]] — score `15`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `14`
- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|README.md]] — score `13`
- [[mql5/Experts/IntermarketDivergence/README|README.md]] — score `13`
- [[docs/architecture|architecture.md]] — score `13`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
