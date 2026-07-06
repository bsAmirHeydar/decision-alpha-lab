
---
type: source_card
source_path: "docs/mql_native/M0001_DISABLE_NODE_PRICE_LINES.md"
source_ext: ".md"
source_size: 734
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Validation / Audit"]
entities: ["M0001"]
---

# Source Card — M0001_DISABLE_NODE_PRICE_LINES.md

## Source

[[docs/mql_native/M0001_DISABLE_NODE_PRICE_LINES|docs/mql_native/M0001_DISABLE_NODE_PRICE_LINES.md]]

## Summary

Full-chart horizontal node price lines are now hard-disabled. Even if `InpShowNodePriceLines` is accidentally left `true` in an old MT5 input set, the Expert forces: and the visual module no longer calls `DAL_DrawHLine()` for node prices. Use local text labels: This draws: HIGH node price above the high-node arrow LOW node price below the low-node arrow Full horizontal lines create heavy chart noise and make node inspection harder. M0001 visual validation should show local node information, not permanent full-chart levels for every node.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001

## Headings

- M0001 Disable Node Price Lines
  - Change
  - Correct way to show node prices
  - Reason

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `12`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `12`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `12`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `12`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `12`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `12`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `12`
- [[docs/mql_native/M0001_EXIT_GAP_BOTH_SIDES_REPAIR|M0001_EXIT_GAP_BOTH_SIDES_REPAIR.md]] — score `12`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001_FAST_FINAL_ONLY_RUNTIME.md]] — score `12`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
