
---
type: source_card
source_path: "docs/mql_native/M0001_NODE_VISIBILITY_DIAGNOSTICS.md"
source_ext: ".md"
source_size: 1185
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "MQL Native", "Validation / Audit"]
entities: ["M0001"]
---

# Source Card — M0001_NODE_VISIBILITY_DIAGNOSTICS.md

## Source

[[docs/mql_native/M0001_NODE_VISIBILITY_DIAGNOSTICS|docs/mql_native/M0001_NODE_VISIBILITY_DIAGNOSTICS.md]]

## Summary

This adds an on-chart diagnostic summary to separate three different questions: Is data limited? Are structural nodes being computed? Are visual caps hiding some computed nodes? The summary now shows: If `nodes` is large and `last_node` is recent, the detector is not capped. If `nodes` is large but `node_draw=latest 2/N`, the cap is visual only. If `last_node` is far behind the current chart time, the L-rule detector has not confirmed a newer structural node yet for the current `InpL`. `InpBars` remains the data cap: Visual caps are separate: `M0001_LiveVisualLab.mq5` version: `1.27`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001

## Headings

- M0001 Node Visibility Diagnostics
  - Purpose
  - New input
  - Summary fields
  - Interpretation
  - Important
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `12`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `12`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `12`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `12`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `12`
- [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|M0001_EXTREME_AND_HUNT_ZONE_AUDIT.md]] — score `12`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md]] — score `12`
- [[docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN|M0001_HUNT_ZONE_FROM_NODE_ORIGIN.md]] — score `12`
- [[docs/mql_native/M0001_JSON_AUDIT_REPORT|M0001_JSON_AUDIT_REPORT.md]] — score `12`
- [[docs/mql_native/M0001_LATEST_VISUAL_CAPS|M0001_LATEST_VISUAL_CAPS.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
