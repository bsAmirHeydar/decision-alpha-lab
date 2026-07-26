
---
type: source_card
source_path: "docs/mql_native/M0001_RTV_FINAL_ONLY_LABELS.md"
source_ext: ".md"
source_size: 565
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Execution / Risk", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_RTV_FINAL_ONLY_LABELS.md

## Source

[[docs/mql_native/M0001_RTV_FINAL_ONLY_LABELS|docs/mql_native/M0001_RTV_FINAL_ONLY_LABELS.md]]

## Summary

RTV is now treated as a final statistic only. A chart label is drawn only when: That means the event must first close by `exit_gap` consecutive candles whose high/low do not intersect the frozen event zone. Until that closure happens, no RTV label is shown. This removes unfinished labels such as: RTV summary mean/median and the text export were already based only on ready RTV events; this change makes the chart labels follow the same final-only rule. Version: `1.51`

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 RTV Final-Only Labels

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
