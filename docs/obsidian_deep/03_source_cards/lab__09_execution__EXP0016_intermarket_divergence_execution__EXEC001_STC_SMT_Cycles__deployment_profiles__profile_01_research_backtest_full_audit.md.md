
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_01_research_backtest_full_audit.md"
source_ext: ".md"
source_size: 1156
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — profile_01_research_backtest_full_audit.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_01_research_backtest_full_audit|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_01_research_backtest_full_audit.md]]

## Summary

Historical validation with all audit outputs and no broker interaction. Runtime mode: Research Backtest. All real transports must be disabled: Real auto-entry: disabled. Broker position manager: disabled or harmless if only audit is needed. Real partial close: disabled. Real hard close finalizer: disabled. Paper Live real-action overrides: disabled. Enable: time audit; check candle audit; W level audit; hunt audit; SMT candidate audit; signal registry audit; paper entry audit; paper outcome audit; paper partial audit; paper hard close audit; persistence snapshot; validation reports. Alerts should not fire for historical backfill. The operator should review: validation summary; time audit; W levels; reference hunts; SMT candidates; signal registry; paper entries; paper outcomes; partial actions; hard close actions. This profile passes when reports are internally consistent and no real bro

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Profile 01 — Research Backtest Full Audit
  - Intent
  - Required mode
  - Real transports
  - Recommended audit settings
  - Expected output
  - Acceptance criteria

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `10`
- [[lab/05_validation/VAL001/report|report.md]] — score `10`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_02_paper_live_observer|profile_02_paper_live_observer.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_03_paper_live_broker_audit|profile_03_paper_live_broker_audit.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_04_auto_trade_entry_only_rehearsal|profile_04_auto_trade_entry_only_rehearsal.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_05_auto_trade_full_managed|profile_05_auto_trade_full_managed.md]] — score `9`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
