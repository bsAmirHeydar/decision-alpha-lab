
---
type: source_card
source_path: "docs/evidence/profile_03_paper_live_broker_audit/b34ade2da6c9_profile_03_paper_live_broker_audit.md"
source_ext: ".md"
source_size: 945
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — profile_03_paper_live_broker_audit.md

## Source

[[docs/evidence/profile_03_paper_live_broker_audit/b34ade2da6c9_profile_03_paper_live_broker_audit|docs/evidence/profile_03_paper_live_broker_audit/b34ade2da6c9_profile_03_paper_live_broker_audit.md]]

## Summary

Live paper monitoring with broker position visibility, but still no real trade management. Runtime mode: Paper Live. Enable broker position manager only for scanning and audit. Real close actions remain disabled. Disabled: Real auto-entry. Real partial close. Real hard close finalizer. Paper Live real-action overrides. The operator should verify: Positions on Symbol1/Symbol2 with the configured magic number are classified as STC-managed. Positions on Symbol1/Symbol2 with other magic numbers are classified as foreign. Foreign positions are never closed. Positions on other symbols are ignored. Broker position rows match actual terminal positions. This profile passes when broker classification is correct and no real close/send action occurs.

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Profile 03 — Paper Live Broker Audit
  - Intent
  - Required mode
  - Broker position manager
  - Real transports
  - What to verify
  - Acceptance criteria

## Related Source Documents

- [[docs/evidence/profile_01_research_backtest_full_audit/b8f8aeb71c39_profile_01_research_backtest_full_audit|profile_01_research_backtest_full_audit.md]] — score `9`
- [[docs/evidence/profile_02_paper_live_observer/a5ba94007b51_profile_02_paper_live_observer|profile_02_paper_live_observer.md]] — score `9`
- [[docs/evidence/profile_04_auto_trade_entry_only_rehearsal/69b400182ebf_profile_04_auto_trade_entry_only_rehearsal|profile_04_auto_trade_entry_only_rehearsal.md]] — score `9`
- [[docs/evidence/profile_05_auto_trade_full_managed/39e8f73f460d_profile_05_auto_trade_full_managed|profile_05_auto_trade_full_managed.md]] — score `9`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] — score `8`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR.md]] — score `8`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER|LEVEL_04_STC_SMT_W_LEVEL_BUILDER.md]] — score `8`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md]] — score `8`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY.md]] — score `8`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
