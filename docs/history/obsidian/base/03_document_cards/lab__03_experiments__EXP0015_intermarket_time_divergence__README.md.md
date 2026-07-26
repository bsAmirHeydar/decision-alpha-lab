---
title: "EXP0015 Intermarket Candle + Session Divergence"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0015_intermarket_time_divergence/README.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "2035"
entities:
  - "EXP0015"
concepts:
  - "Intermarket Divergence"
  - "Licensing"
  - "MQL Native"
  - "NDS Anatomy"
---


# EXP0015 Intermarket Candle + Session Divergence

**Source:** [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|lab/03_experiments/EXP0015_intermarket_time_divergence/README.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `2035` bytes

## خلاصه

This experiment detects two-symbol divergence with both candle-based and session-based reference levels. `previous_candle` `rolling` `current_session` `previous_session` `wick_touch` `close_break` `hunt_reject_close` Required CSV schema: Run: Outputs: The live path is intentionally decoupled: The MQL5 expert can read the same normalized CSV files repeatedly in timer mode. This keeps raw data-feed authentication and WebSocket/reconnect logic outside MQL5. The complete English setup guide for live, historical, delayed fallback, and five-minute historical polling is here: Most useful commands:

## Headings

- EXP0015 Intermarket Candle + Session Divergence
-   Current level families
-   Trigger modes
-   Backtest from normalized CSV
-   Live bridge path
-   CME bridge guide
- Licensed CME historical download through Databento
- Licensed CME live stream through Databento
- Near-live closed-bar historical polling every 5 minutes
- Development fallback without CME credentials

## Entities

`EXP0015`

## Concepts

- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[tools/cme_bridge/README|DAL CME Bridge for EXP0015]] — `tool_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|Offline License Layer - EXEC001 STC SMT Cycles]] — `experiment`
- [[mql5/Experts/IntermarketDivergence/README|Intermarket Divergence Experts]] — `mql5_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[mql5/Experts/IntermarketDivergenceExecution/README|Intermarket Divergence Execution Experts]] — `mql5_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[README|Decision Alpha Lab]] — `readme`
- [[tools/astro_live_bridge/README|EXP0013 Astro Live Bridge V2]] — `tool_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/README|EXEC001 STC SMT Cycles — Deployment Profiles]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
