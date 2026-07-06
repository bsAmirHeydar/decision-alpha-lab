
---
type: source_card
source_path: "docs/mql_native/M0001_CONSUMED_ZONE_HISTORY.md"
source_ext: ".md"
source_size: 734
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_CONSUMED_ZONE_HISTORY.md

## Source

[[docs/mql_native/M0001_CONSUMED_ZONE_HISTORY|docs/mql_native/M0001_CONSUMED_ZONE_HISTORY.md]]

## Summary

When a node is consumed, the live decision process is finished, but the historical hunt/territory rectangle should remain visible on the chart up to the consume candle. Active node: Consumed node: The zone does not extend after consumption. Set it to `false` to hide consumed zones completely. Expansion extreme remains a live variable only while the node is active. The zone history is kept for visual audit, not because the node remains active. Version: `1.23`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Consumed Zone History
  - Rule
  - Behavior
  - Input
  - Important

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `12`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `12`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `12`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `12`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `12`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `12`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `12`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `12`
- [[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|M0001_CONSUMED_NODE_REPAIR.md]] — score `12`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
