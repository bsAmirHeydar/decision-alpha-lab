
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/02_normalized_strategy_spec.md"
source_ext: ".md"
source_size: 8595
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 02_normalized_strategy_spec.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/02_normalized_strategy_spec|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/02_normalized_strategy_spec.md]]

## Summary

Strategy ID: `EXEC001_STC_SMT_CYCLES` Strategy family: Intermarket divergence execution. Primary signal type: SMT divergence between two index symbols. Default symbols: Symbol1: `SPXUSD` Symbol2: `NDXUSD` The same logic applies to equivalent pairs such as `SPX/NDX`, `US500/NAS100`, `ES/NQ`, or broker-specific equivalents. The code must treat `Symbol1` and `Symbol2` as both data symbols and execution symbols for this strat… The EA may be attached to any chart. The chart symbol does not define the strategy universe. All analysis and execution use only `Symbol1` and `Symbol2`. The EA must block duplicate active instances for the same strategy ID and symbol pair. This prevents double entries if the user accidentally attaches the same EA to multiple charts. The STC trading day is defined in New York time. Start: 20:00 New York. End: 15:30 New York on the following calendar day. Hard reset: 15

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 02 - Normalized Strategy Specification
  - 1. Strategy identity
  - 2. Runtime independence
  - 3. Trading day
  - 4. M cycles and no-entry gaps
  - 5. W cycles
  - 6. Reference matrix
  - 7. Structural two-symbol comparison
  - 8. Hunt definition
  - 9. Side mapping
  - 10. Confirmation
  - 11. Check candle construction

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `10`
- [[lab/05_validation/VAL001/report|report.md]] — score `10`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/04_smt_divergence_rules|04_smt_divergence_rules.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk|05_execution_and_risk.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `9`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
