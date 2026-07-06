
---
type: source_card
source_path: "docs/mql_native/M0001_REVISIT_EXTREME_RESET.md"
source_ext: ".md"
source_size: 1708
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "MQL Native", "UI / React", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_REVISIT_EXTREME_RESET.md

## Source

[[docs/mql_native/M0001_REVISIT_EXTREME_RESET|docs/mql_native/M0001_REVISIT_EXTREME_RESET.md]]

## Summary

A revisited live node is not measured forever from the original node origin. After a confirmed revisit in HUNT mode, the node remains alive with memory, but its next expansion/territory cycle resets. The node is still the same structural node, but the market has already tested its territory. For the next revisit, we want to know the expansion from the last confirmed visit forward, not from the original node candle. Before any confirmed revisit: When: the visit is confirmed. If the node is not consumed: Then the next territory is built from that reset extreme. TOUCH mode consumes after the first confirmed touch, so there is no post-touch revisit cycle. If HUNT happens before confirmation, the node is consumed by HUNT. A revisited live label now includes reset anchor index: `reset@1234` is the bar index where the current post-visit tracking cycle starts. `M0001_LiveVisualLab.mq5` version:

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Revisit Extreme Reset
  - Decision
  - Why
  - First cycle
  - After each confirmed revisit in HUNT mode
  - TOUCH mode
  - Visual
  - Version

## Related Source Documents

- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `18`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `18`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `18`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `18`
- [[docs/architecture|architecture.md]] — score `17`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `17`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `17`
- [[docs/execution/README|README.md]] — score `17`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `17`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
