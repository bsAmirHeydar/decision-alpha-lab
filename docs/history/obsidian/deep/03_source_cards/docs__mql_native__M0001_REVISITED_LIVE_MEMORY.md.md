
---
type: source_card
source_path: "docs/mql_native/M0001_REVISITED_LIVE_MEMORY.md"
source_ext: ".md"
source_size: 2027
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "MQL Native", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_REVISITED_LIVE_MEMORY.md

## Source

[[docs/mql_native/M0001_REVISITED_LIVE_MEMORY|docs/mql_native/M0001_REVISITED_LIVE_MEMORY.md]]

## Summary

A revisit does not have to happen immediately after the previous event. In HUNT consumption mode, a confirmed touch does not kill the node. The node returns to normal tracking and can be revisited much later. A node is fresh while it is alive and has no confirmed revisit: Visual label: In TOUCH mode: When price enters the live territory zone, the next revisit starts: Visual label: In TOUCH mode: A pending revisit becomes confirmed only after: In HUNT mode, confirmation stores memory and returns the node to tracking: The next revisit can happen many candles later. Visual label: `age` is the number of bars since the last confirmed revisit. In TOUCH mode: There is no true multi-revisit loop in TOUCH mode. In HUNT mode: The consumed label keeps the number of confirmed revisits before death: A revisited live node is not the same as a virgin node. It is still live, but the market has already i

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Revisited Live Memory
  - Core idea
  - Fresh live node
  - Pending revisit
  - Confirmed revisit
  - Consumption
  - Why this matters
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `16`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `16`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `16`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001_FULL_REVISIT_LOGIC.md]] — score `16`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001_MINIMAL_INPUTS.md]] — score `16`
- [[docs/mql_native/M0001_REVISIT_EXTREME_RESET|M0001_REVISIT_EXTREME_RESET.md]] — score `16`
- [[docs/mql_native/M0001_RTV_LOG_HILO|M0001_RTV_LOG_HILO.md]] — score `16`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001_VIEWPORT_VISUAL_RENDERER.md]] — score `16`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `16`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
