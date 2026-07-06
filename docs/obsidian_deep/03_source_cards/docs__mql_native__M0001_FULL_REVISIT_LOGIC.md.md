
---
type: source_card
source_path: "docs/mql_native/M0001_FULL_REVISIT_LOGIC.md"
source_ext: ".md"
source_size: 1862
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "MQL Native", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_FULL_REVISIT_LOGIC.md

## Source

[[docs/mql_native/M0001_FULL_REVISIT_LOGIC|docs/mql_native/M0001_FULL_REVISIT_LOGIC.md]]

## Summary

A revisit is a completed territory interaction event for a node that has not yet been consumed. A revisit starts when a candle intersects the current live territory zone: At this exact entry candle, event geometry freezes: While the event is active: This prevents the current revisit from repainting, while still keeping the node's future territory correct if the node remains alive. A pending touch becomes confirmed only after: using the frozen event zone. HUNT always has priority before touch confirmation: If this happens during a pending revisit, that revisit closes as HUNT and the node is consumed by HUNT. TOUCH mode: HUNT mode: New visual inputs: Labels: `M0001_LiveVisualLab.mq5` version: `1.40`.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Full Revisit Logic
  - Revisit definition
  - Start condition
  - Active event
  - Touch confirmation
  - HUNT priority
  - Consumption modes
  - Visuals
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `16`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `16`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `16`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001_MINIMAL_INPUTS.md]] — score `16`
- [[docs/mql_native/M0001_REVISIT_EXTREME_RESET|M0001_REVISIT_EXTREME_RESET.md]] — score `16`
- [[docs/mql_native/M0001_REVISITED_LIVE_MEMORY|M0001_REVISITED_LIVE_MEMORY.md]] — score `16`
- [[docs/mql_native/M0001_RTV_LOG_HILO|M0001_RTV_LOG_HILO.md]] — score `16`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001_VIEWPORT_VISUAL_RENDERER.md]] — score `16`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `16`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
