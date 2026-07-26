
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_21_STC_SMT_DRAWING_AUDIT.md"
source_ext: ".md"
source_size: 809
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Execution / Risk", "Intermarket Divergence", "Validation / Audit"]
entities: []
---

# Source Card — LEVEL_21_STC_SMT_DRAWING_AUDIT.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_21_STC_SMT_DRAWING_AUDIT|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_21_STC_SMT_DRAWING_AUDIT.md]]

## Summary

Level 21 is a visual verification patch for `EXEC001_STC_SMT_Cycles`. It improves the chart overlay so an operator can verify the locked STC rules directly on the active `Symbol1` or `Symbol2` chart: New York STC session structure. M cycles and no-entry gaps. W boundaries and closed W high/low levels. Recent check-candle boxes. W1 no-signal and final-check no-entry conditions. Raw previous-W hunt markers. BOTH-hunted no-SMT cases. Clean-symbol SMT side and selected reference. Paper entry, SL, TP, W4 partial marker, 15:30 hard-close marker and outcome labels. No trading logic changes were made. The patch also fixes the hard-close compile warning by explicitly casting `SYMBOL_SPREAD` to `double` before reporting cost calculations.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- LEVEL 21 — STC SMT Drawing Audit Hardening

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `10`
- [[lab/05_validation/VAL001/report|report.md]] — score `10`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `10`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `9`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015_cme_live_backtest_plan.md]] — score `8`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `8`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `8`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
