
---
type: source_card
source_path: "docs/mql_native/M0001_MQL_NATIVE_SPEC.md"
source_ext: ".md"
source_size: 897
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_MQL_NATIVE_SPEC.md

## Source

[[docs/mql_native/M0001_MQL_NATIVE_SPEC|docs/mql_native/M0001_MQL_NATIVE_SPEC.md]]

## Summary

A node at index `i` is confirmed only when `L` right-side candles exist. For `L = 5`: The node is available in a live-safe stream when: The visual marker is drawn on the pivot candle, not on the confirmation candle. For each confirmed node: Start scanning from `active_from_index = node_index + L`. Expand the opposite extreme. Build a territory around the node price. Start an event when a candle intersects the territory. Close the event after `exit_gap` outside candles. Compute: The native Expert reads candles directly from MT5. No external bridge, file watcher, or asynchronous process is involved.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 MQL-Native Specification
  - L-rule node
  - RTV event
  - Runtime Guarantee

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `14`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `14`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `14`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `14`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `14`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `14`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md]] — score `14`
- [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|M0001_H0001_LOGIC_REPAIR_AUDIT.md]] — score `14`
- [[docs/mql_native/M0001_LIVE_ZONE_RESYNC|M0001_LIVE_ZONE_RESYNC.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
