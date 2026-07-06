
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/07_test_plan.md"
source_ext: ".md"
source_size: 5371
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 07_test_plan.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/07_test_plan|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/07_test_plan.md]]

## Summary

The test plan ensures the STC SMT Cycles implementation follows the locked specification before any live trading. Every test should be deterministic and should write expected vs actual values to a report. Test M assignment: 20:00 is M1. 01:59 is M1. 02:00 is gap. 02:59 is gap. 03:00 is M2. 08:59 is M2. 09:00 is gap. 09:29 is gap. 09:30 is M3. 15:29 is M3. 15:30 is hard close/reset. Test W assignment for every W in M1, M2, and M3. Test DST transition dates using New York time. For each check timeframe, verify aggregation starts at 20:00 New York. Examples: 10m: 20:00-20:10. 10m: 21:20-21:30. 15m: 20:00-20:15. 3m: 20:00-20:03. Verify that final check candles ending at M boundaries cannot enter. Build synthetic M1 data and verify W high/low: W high equals maximum high inside the W. W low equals minimum low inside the W. W completeness fails if either symbol is missing required data. W1 prod

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 07 - Test Plan
  - 1. Purpose
  - 2. Time and cycle tests
  - 3. Check candle anchoring tests
  - 4. W level tests
  - 5. Reference matrix tests
  - 6. Hunt tests
  - 7. SMT divergence tests
  - 8. Confirmation tests
  - 9. Reference selection tests
  - 10. Ambiguity tests
  - 11. Risk tests

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `10`
- [[lab/05_validation/VAL001/report|report.md]] — score `10`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/02_normalized_strategy_spec|02_normalized_strategy_spec.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/04_smt_divergence_rules|04_smt_divergence_rules.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk|05_execution_and_risk.md]] — score `9`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
