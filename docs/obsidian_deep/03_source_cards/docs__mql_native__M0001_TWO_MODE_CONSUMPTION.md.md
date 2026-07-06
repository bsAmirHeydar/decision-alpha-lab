
---
type: source_card
source_path: "docs/mql_native/M0001_TWO_MODE_CONSUMPTION.md"
source_ext: ".md"
source_size: 1391
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "MQL Native", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_TWO_MODE_CONSUMPTION.md

## Source

[[docs/mql_native/M0001_TWO_MODE_CONSUMPTION|docs/mql_native/M0001_TWO_MODE_CONSUMPTION.md]]

## Summary

M0001 node consumption is now explicit and two-mode: or: Legacy alias is kept: If `InpConsumeOnTouch=true`, it forces touch-zone mode. Zone touches do not consume the node. The node remains active until its actual price level is broken. The node is consumed on the first candle that intersects its current territory zone. When consumed by touch, the audit extreme and zone history are frozen at the touch candle. They remain visible as history but do not keep updating. This is not just a visual change. `DAL_M0001ComputeNodeAuditStates()` now applies the selected consume mode while tracking each node live. `DAL_M0001ComputeEvents()` also records consumed state, consumed index/time, and consume reason for event journals. Consumed markers now show: `M0001_LiveVisualLab.mq5` version: `1.29`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Two-Mode Node Consumption
  - Purpose
  - Inputs
  - Mode 1: hunt / node break
  - Mode 2: touch zone
  - Underlying code changes
  - Visual change
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `14`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `14`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `14`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `14`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|M0001_EXTREME_AND_HUNT_ZONE_AUDIT.md]] — score `14`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md]] — score `14`
- [[docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN|M0001_HUNT_ZONE_FROM_NODE_ORIGIN.md]] — score `14`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001_JSON_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON|M0001_LOGRTV_RANDOM_NULL_COMPARISON.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
