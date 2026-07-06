
---
type: source_card
source_path: "docs/mql_native/M0001_RTV_WAIT_FOR_EXIT_GAP.md"
source_ext: ".md"
source_size: 964
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "MQL Native", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_RTV_WAIT_FOR_EXIT_GAP.md

## Source

[[docs/mql_native/M0001_RTV_WAIT_FOR_EXIT_GAP|docs/mql_native/M0001_RTV_WAIT_FOR_EXIT_GAP.md]]

## Summary

RTV is calculated only after the event has actually closed by exit-gap: Any candle that intersects the frozen zone resets the outside counter. So HUNT-before-confirmation events can still exist for visual audit, but they are not included in RTV mean/median and are written as non-ready/n/a. After exit-gap closure: The final outside confirmation candles are not included in the inside volatility sample. `M0001_LiveVisualLab.mq5` version: `1.50`.

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 RTV Waits for Exit-Gap Closure
  - Rule
  - RTV-ready condition
  - Sample construction
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `14`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `14`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `14`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `14`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md]] — score `14`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001_JSON_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON|M0001_LOGRTV_RANDOM_NULL_COMPARISON.md]] — score `14`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001_MINIMAL_INPUTS.md]] — score `14`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
