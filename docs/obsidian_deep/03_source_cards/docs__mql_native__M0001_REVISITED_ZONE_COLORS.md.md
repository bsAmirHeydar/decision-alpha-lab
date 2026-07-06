
---
type: source_card
source_path: "docs/mql_native/M0001_REVISITED_ZONE_COLORS.md"
source_ext: ".md"
source_size: 456
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_REVISITED_ZONE_COLORS.md

## Source

[[docs/mql_native/M0001_REVISITED_ZONE_COLORS|docs/mql_native/M0001_REVISITED_ZONE_COLORS.md]]

## Summary

When a node survives and receives at least one confirmed revisit, its live zone rectangle changes color: HIGH / peak revisited zone -> purple LOW / valley revisited zone -> blue Rules: Fresh live zones keep the normal node-side colors. Consumed zones still fall back to the consumed/inactive gray history style. Only the rectangle color changes; the revisit logic and state model are unchanged. Version: `1.47`

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Revisited Zone Colors

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `10`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `10`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `10`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `10`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `10`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `10`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `10`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `10`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001_CLEAN_REVISIT_LABELS.md]] — score `10`
- [[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|M0001_CONSUMED_NODE_REPAIR.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
