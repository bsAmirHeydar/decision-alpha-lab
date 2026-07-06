
---
type: source_card
source_path: "lab/03_experiments/EXP0015_intermarket_time_divergence/README.md"
source_ext: ".md"
source_size: 2035
empty: false
generated_at: 2026-07-06
concepts: ["Intermarket Divergence", "Licensing", "MQL Native", "Python Brain", "UI / React"]
entities: ["EXP0015"]
---

# Source Card — README.md

## Source

[[lab/03_experiments/EXP0015_intermarket_time_divergence/README|lab/03_experiments/EXP0015_intermarket_time_divergence/README.md]]

## Summary

This experiment detects two-symbol divergence with both candle-based and session-based reference levels. `previous_candle` `rolling` `current_session` `previous_session` `wick_touch` `close_break` `hunt_reject_close` Required CSV schema: Run: Outputs: The live path is intentionally decoupled: The MQL5 expert can read the same normalized CSV files repeatedly in timer mode. This keeps raw data-feed authentication and WebSocket/reconnect logic outside MQL5. The complete English setup guide for live, historical, delayed fallback, and five-minute historical polling is here: Most useful commands:

## Concepts

[[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0015

## Headings

- EXP0015 Intermarket Candle + Session Divergence
  - Current level families
  - Trigger modes
  - Backtest from normalized CSV
  - Live bridge path
  - CME bridge guide
- Licensed CME historical download through Databento
- Licensed CME live stream through Databento
- Near-live closed-bar historical polling every 5 minutes
- Development fallback without CME credentials

## Related Source Documents

- [[tools/cme_bridge/README|README.md]] — score `23`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|README.md]] — score `21`
- [[mql5/Experts/IntermarketDivergence/README|README.md]] — score `19`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `16`
- [[mql5/Experts/IntermarketDivergenceExecution/README|README.md]] — score `16`
- [[docs/flag_counting/README|README.md]] — score `16`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `16`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|README.md]] — score `16`
- [[mql5/Experts/AstroExecution/README|README.md]] — score `16`
- [[tools/astro_live_bridge/README|README.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
