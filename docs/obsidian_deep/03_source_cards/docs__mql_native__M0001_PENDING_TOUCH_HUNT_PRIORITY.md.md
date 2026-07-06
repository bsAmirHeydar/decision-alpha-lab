
---
type: source_card
source_path: "docs/mql_native/M0001_PENDING_TOUCH_HUNT_PRIORITY.md"
source_ext: ".md"
source_size: 1081
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_PENDING_TOUCH_HUNT_PRIORITY.md

## Source

[[docs/mql_native/M0001_PENDING_TOUCH_HUNT_PRIORITY|docs/mql_native/M0001_PENDING_TOUCH_HUNT_PRIORITY.md]]

## Summary

A zone touch is not immediately a confirmed TOUCH consumption. It is first a pending touch / active event. During this pending event, the node can still be hunted. HUNT always has priority over TOUCH while a touch event is pending. For a LOW node: For a HIGH node: TOUCH is confirmed only after: using the frozen event territory from the first touch candle. This keeps the state machine faithful to the intended model: `M0001_LiveVisualLab.mq5` version: `1.31`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Pending Touch and Hunt Priority
  - Correction
  - Priority
  - TOUCH confirmation
  - Why
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
