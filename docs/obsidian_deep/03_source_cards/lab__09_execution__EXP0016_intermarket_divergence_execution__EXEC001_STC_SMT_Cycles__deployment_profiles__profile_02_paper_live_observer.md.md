
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_02_paper_live_observer.md"
source_ext: ".md"
source_size: 853
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — profile_02_paper_live_observer.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_02_paper_live_observer|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/profile_02_paper_live_observer.md]]

## Summary

Run the live STC logic without broker interaction. Runtime mode: Paper Live. Disabled: Real auto-entry. Real partial close. Real hard close finalizer. Broker close actions. Broker position manager should normally be off in this profile. Enable: signal alerts; paper entry alerts; paper outcome alerts; partial paper alerts; hard close paper alerts; ambiguity alerts. Disable replay-on-init unless debugging. Drawing should normally be enabled so that the operator can visually compare: M/W boundaries; W high/low levels; check candle state; entry/SL/TP; partial and hard close markers. This profile passes when live alerts match the CSV rows and no real broker action occurs.

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Profile 02 — Paper Live Observer
  - Intent
  - Required mode
  - Real transports
  - Alerts
  - Drawing
  - Acceptance criteria

## Related Source Documents

- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] — score `10`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR.md]] — score `10`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER|LEVEL_04_STC_SMT_W_LEVEL_BUILDER.md]] — score `10`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md]] — score `10`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY.md]] — score `10`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `10`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_19_STC_SMT_VALIDATION_PACK|LEVEL_19_STC_SMT_VALIDATION_PACK.md]] — score `10`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015_cme_live_backtest_plan.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
