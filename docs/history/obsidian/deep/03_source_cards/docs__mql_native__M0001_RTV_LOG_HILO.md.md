
---
type: source_card
source_path: "docs/mql_native/M0001_RTV_LOG_HILO.md"
source_ext: ".md"
source_size: 1353
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "MQL Native", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_RTV_LOG_HILO.md

## Source

[[docs/mql_native/M0001_RTV_LOG_HILO|docs/mql_native/M0001_RTV_LOG_HILO.md]]

## Summary

For each candle: For each event/revisit: When a touch is confirmed by `exit_gap` consecutive candles outside the frozen event zone, those final outside confirmation candles are not counted in the RTV inside sample. So if: then: The outside confirmation bars `107..112` confirm that the event is over, but they are not part of the volatility sample being measured inside the territory event. If a node is hunted before touch confirmation, no exit-gap exclusion is applied: `InpShowRTV` controls RTV labels: Labels: `RTV n/a` appears when there are not enough baseline candles before entry. `M0001_LiveVisualLab.mq5` version: `1.48`.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 RTV — Log High/Low Volatility
  - Formula
  - Exit-gap exclusion
  - HUNT before confirmation
  - Visual
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `18`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `18`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `18`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001_MINIMAL_INPUTS.md]] — score `18`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001_VIEWPORT_VISUAL_RENDERER.md]] — score `18`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `18`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `18`
- [[docs/architecture|architecture.md]] — score `17`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `17`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
