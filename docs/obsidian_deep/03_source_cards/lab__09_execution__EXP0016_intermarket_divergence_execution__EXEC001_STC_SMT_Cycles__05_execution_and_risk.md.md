
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk.md"
source_ext: ".md"
source_size: 6479
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 05_execution_and_risk.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk.md]]

## Summary

Backtest: The strategy confirms at the close of a check candle. Entry price is the open of the next check candle. If there is no next check candle inside the same M, no entry is allowed. Live/paper: Entry is a market order immediately after the confirmation check candle closes. If the EA is offline at the exact entry time, no delayed entry is allowed. If Entry STC is ON, confirmed signals may execute. If Entry STC is OFF: The signal is audited. No trade is opened. The signal is consumed for trading. The strategy must not enter later if Entry STC is turned ON. Existing positions continue to be managed. The trade is always opened on the clean symbol that did not hunt. The strategy uses `Symbol1` and `Symbol2` as both signal symbols and execution symbols. Buy trade: Stop loss is the selected reference W low of the trade symbol. Sell trade: Stop loss is the selected reference W high of the t

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 05 - Execution, Risk, Position Management, and Outcomes
  - 1. Entry model
  - 2. Entry STC switch
  - 3. Trade symbol
  - 4. Stop loss
  - 5. Target
  - 6. Risk sizing
  - 7. Broker volume limits
  - 8. Order failure
  - 9. Trade counter
  - 10. Hedging OFF
  - 11. Hedging ON

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `12`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13_data_model_and_journals.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/16_implementation_checklist|16_implementation_checklist.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
