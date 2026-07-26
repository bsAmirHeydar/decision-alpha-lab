
---
type: source_card
source_path: "docs/M0001_NODE_REVEAL_TIMING_FIX.md"
source_ext: ".md"
source_size: 1025
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Python Brain", "Validation / Audit"]
entities: ["M0001"]
---

# Source Card — M0001_NODE_REVEAL_TIMING_FIX.md

## Source

[[docs/M0001_NODE_REVEAL_TIMING_FIX|docs/M0001_NODE_REVEAL_TIMING_FIX.md]]

## Summary

In a live-safe L-rule detector, a node located at candle `i` is not knowable at candle `i`. It becomes knowable only after `L` right-side candles exist: If the visual marker is always drawn back on `node_index`, the chart can feel like it is backpainting: the marker appears late but is placed on the older pivot candle. The Python visual contract now sends both times for every node: The MQL visual terminal can choose how to draw node markers: Default is `1`, which matches live decision semantics: the marker appears at the time the node becomes knowable. The node price remains the original Python node price in both modes. Only the marker time changes.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001

## Headings

- M0001 Node Reveal Timing Fix
  - Problem
  - Fix
  - Important

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `12`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001_EVENT_BRIDGE_ARCHITECTURE.md]] — score `12`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `12`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `12`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `12`
- [[docs/mql_live_visual_lab_debug_packages|mql_live_visual_lab_debug_packages.md]] — score `12`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL_NATIVE_MIGRATION_DECISION.md]] — score `12`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `12`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `11`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
