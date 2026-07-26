
---
type: source_card
source_path: "docs/evidence/14_backtest_live_runtime/c31f0574e3ec_14_backtest_live_runtime.md"
source_ext: ".md"
source_size: 3479
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 14_backtest_live_runtime.md

## Source

[[docs/evidence/14_backtest_live_runtime/c31f0574e3ec_14_backtest_live_runtime|docs/evidence/14_backtest_live_runtime/c31f0574e3ec_14_backtest_live_runtime.md]]

## Summary

The implementation should support three modes: Research backtest. Paper live. Auto trade. The first build should prioritize research backtest and paper live. Auto trade should be enabled only after deterministic tests pass. Backtest loop: Load Symbol1 and Symbol2 bars. Convert timestamps to New York time. Build STC trading days. For each day, build M/W structure. Build check candles anchored at 20:00. Process completed check candles in chronological order. Detect and confirm SMT. Create simulated entries at next check-candle open. Simulate SL/TP/ambiguous outcomes using check-candle bars. Apply partial and hard close rules. Write journals and summary. Both symbols must have complete data for signal decisions. If either symbol is missing data for a required W or check candle, no trade is allowed for that decision point. Missing data must be logged. If signal confirms at check candle close

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 14 - Backtest and Live Runtime
  - 1. Runtime modes
  - 2. Research backtest runtime
  - 3. Backtest data requirements
  - 4. Backtest entry timing
  - 5. Backtest outcome timing
  - 6. Paper live runtime
  - 7. Auto-trade runtime
  - 8. Live entry failure
  - 9. Offline-at-entry behavior
  - 10. Delayed actions allowed
  - 11. Runtime safety rules

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `14`
- [requirements.txt](../../tools/cme_bridge/requirements.txt) — score `12`
- [requirements.txt](../../requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_feature_builder/requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_ml/requirements.txt) — score `10`
- [[docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec|02_normalized_strategy_spec.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `9`
- [[docs/evidence/04_smt_divergence_rules_algorithms/5dba5ebb5e42_04_smt_divergence_rules|04_smt_divergence_rules.md]] — score `9`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05_execution_and_risk.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `9`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
