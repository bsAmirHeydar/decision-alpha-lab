
---
type: source_card
source_path: "docs/mql_native/M0001_CONSUMED_EXTREME_HISTORY.md"
source_ext: ".md"
source_size: 864
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Validation / Audit"]
entities: ["M0001"]
---

# Source Card — M0001_CONSUMED_EXTREME_HISTORY.md

## Source

[[docs/mql_native/M0001_CONSUMED_EXTREME_HISTORY|docs/mql_native/M0001_CONSUMED_EXTREME_HISTORY.md]]

## Summary

When a node is consumed, its expansion extreme is no longer a live variable. However, the final node-to-extreme link should remain visible as history. Active node: Consumed node: The line does not extend or update after the consume candle. Set to `false` to hide consumed-node extreme links entirely. This is not only a drawing rule. The audit-state engine already stops scanning the node once it is consumed, so the stored `expansion_extreme` is frozen at the final meaningful point. The visual layer now keeps that frozen final link on the chart for audit. Version: `1.24`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001

## Headings

- M0001 Consumed Extreme History
  - Rule
  - Behavior
  - Input
  - Logic vs visual

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
