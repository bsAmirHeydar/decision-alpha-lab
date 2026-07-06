
---
type: source_card
source_path: "docs/mql_native/M0001_NODE_PRICE_LABELS.md"
source_ext: ".md"
source_size: 796
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node"]
entities: ["M0001"]
---

# Source Card — M0001_NODE_PRICE_LABELS.md

## Source

[[docs/mql_native/M0001_NODE_PRICE_LABELS|docs/mql_native/M0001_NODE_PRICE_LABELS.md]]

## Summary

`InpShowNodePrices` no longer draws full-chart horizontal lines. It now draws a local text label near the node marker: HIGH node: price text above the red chevron LOW node: price text below the green chevron This keeps the chart clean while still showing the exact node price. The old full-chart line behavior is still available separately: Default: Full horizontal node-price lines create visual noise and can make structural inspection harder on M1/M5 charts. Local labels keep the chart readable and make each node's exact price obvious.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]]

## Entities

M0001

## Headings

- M0001 Node Price Labels
  - Change
  - Inputs
  - Reason

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `10`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `10`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `10`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `10`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `10`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `10`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `10`
- [[docs/mql_native/M0001_CLEAN_ARROW_MARKERS|M0001_CLEAN_ARROW_MARKERS.md]] — score `10`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001_CLEAN_REVISIT_LABELS.md]] — score `10`
- [[docs/mql_native/M0001_DISABLE_NODE_PRICE_LINES|M0001_DISABLE_NODE_PRICE_LINES.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
