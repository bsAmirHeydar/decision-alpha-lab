
---
type: source_card
source_path: "docs/evidence/profile_06_emergency_hard_close_only/e564656d4633_profile_06_emergency_hard_close_only.md"
source_ext: ".md"
source_size: 932
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "UI / React"]
entities: []
---

# Source Card — profile_06_emergency_hard_close_only.md

## Source

[[docs/evidence/profile_06_emergency_hard_close_only/e564656d4633_profile_06_emergency_hard_close_only|docs/evidence/profile_06_emergency_hard_close_only/e564656d4633_profile_06_emergency_hard_close_only.md]]

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
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `10`
- [[docs/evidence/exp0000_sample/58c8a635ff91_report|report.md]] — score `8`
- [[docs/evidence/exp0001_structural_highs_lows_importance/337872464ffa_report|report.md]] — score `8`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|report.md]] — score `8`
- [[docs/evidence/val001/360462a17ab1_report|report.md]] — score `8`
- [[docs/evidence/profile_01_research_backtest_full_audit/b8f8aeb71c39_profile_01_research_backtest_full_audit|profile_01_research_backtest_full_audit.md]] — score `7`
- [[docs/evidence/profile_02_paper_live_observer/a5ba94007b51_profile_02_paper_live_observer|profile_02_paper_live_observer.md]] — score `7`
- [[docs/evidence/profile_03_paper_live_broker_audit/b34ade2da6c9_profile_03_paper_live_broker_audit|profile_03_paper_live_broker_audit.md]] — score `7`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
