
---
type: source_card
source_path: "docs/mql_native/M0001_RTV_SUMMARY_TEXT.md"
source_ext: ".md"
source_size: 827
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_RTV_SUMMARY_TEXT.md

## Source

[[docs/mql_native/M0001_RTV_SUMMARY_TEXT|docs/mql_native/M0001_RTV_SUMMARY_TEXT.md]]

## Summary

Every M0001 run now updates the chart comment with the final ready RTV summary: Only events with `rtv_ready=true` are included. The EA writes all final ready RTV rows into a text file: The writer first attempts the common terminal files area using `FILE_COMMON`, then falls back to the terminal-local `MQL5/Files` directory. Each ready RTV event row includes: `M0001_LiveVisualLab.mq5` version: `1.49`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 RTV Summary Comment and Text File
  - Chart comment
  - Text file
  - Included rows
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `14`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `14`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `14`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `14`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md]] — score `14`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001_FULL_REVISIT_LOGIC.md]] — score `14`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001_JSON_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_LIVE_ZONE_RESYNC|M0001_LIVE_ZONE_RESYNC.md]] — score `14`
- [[docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON|M0001_LOGRTV_RANDOM_NULL_COMPARISON.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
