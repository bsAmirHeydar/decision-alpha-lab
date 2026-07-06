
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_06_emergency_hard_close_only.md"
source_ext: ".md"
source_size: 932
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "UI / React"]
entities: []
---

# Source Card — profile_06_emergency_hard_close_only.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_06_emergency_hard_close_only|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_06_emergency_hard_close_only.md]]

## Summary

Close remaining STC-managed positions after 15:30 New York without allowing new entries. Disable: STC entry. Real auto-entry. Real partial close. Enable: Broker position manager. Real hard close finalizer. The finalizer must only close positions that: are on Symbol1 or Symbol2; match the configured magic number; are still open after the STC hard-close threshold. Manual or foreign positions must never be closed. Use this profile when: the EA was restarted after 15:30; managed positions remain open unexpectedly; auto-entry must stay disabled while cleanup is performed; the operator wants finalizer-only behavior. The profile passes when all matching magic-number positions are closed or clearly reported as requiring manual review after retry cap.

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- Profile 06 — Emergency Hard Close Only
  - Intent
  - Required behavior
  - Important constraints
  - Use cases
  - Acceptance criteria

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `10`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `10`
- [[lab/03_experiments/EXP0000_sample/report|report.md]] — score `8`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|report.md]] — score `8`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `8`
- [[lab/05_validation/VAL001/report|report.md]] — score `8`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_01_research_backtest_full_audit|profile_01_research_backtest_full_audit.md]] — score `7`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_02_paper_live_observer|profile_02_paper_live_observer.md]] — score `7`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_03_paper_live_broker_audit|profile_03_paper_live_broker_audit.md]] — score `7`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
