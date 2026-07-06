
---
type: source_card
source_path: "docs/mql_native/M0001_UNBOUNDED_BACKTEST_DATA.md"
source_ext: ".md"
source_size: 1220
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Validation / Audit"]
entities: ["M0001"]
---

# Source Card — M0001_UNBOUNDED_BACKTEST_DATA.md

## Source

[[docs/mql_native/M0001_UNBOUNDED_BACKTEST_DATA|docs/mql_native/M0001_UNBOUNDED_BACKTEST_DATA.md]]

## Summary

Backtests are no longer limited by an arbitrary candle count. Default: Meaning: If you want a rolling cap for performance, set: or any positive number. `DAL_AppendBarChronological()` now treats `max_bars <= 0` as unbounded. It keeps every newly closed candle in chronological order and does not drop old candles. This means Strategy Tester controls the sample using its own symbol/timeframe/date range, not the EA. `DAL_LoadBarsChronological()` also treats `requested_bars <= 0` as all available bars from `Bars(symbol, timeframe)`, instead of falling back to 500. Default computed event cap is now: Meaning unlimited computed events. Visual caps are also zero by default: Meaning draw all audit objects. For very long tests, set positive draw caps if the chart becomes slow. `M0001_LiveVisualLab.mq5` version: `1.25`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001

## Headings

- M0001 Unbounded Backtest Data
  - Change
  - Live stream behavior
  - Fallback bulk loader
  - Computation limits
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `14`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `14`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `14`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `14`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md]] — score `14`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001_JSON_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_LATEST_VISUAL_CAPS|M0001_LATEST_VISUAL_CAPS.md]] — score `14`
- [[docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON|M0001_LOGRTV_RANDOM_NULL_COMPARISON.md]] — score `14`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001_MINIMAL_INPUTS.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
