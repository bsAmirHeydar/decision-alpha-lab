
---
type: source_card
source_path: "docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX.md"
source_ext: ".md"
source_size: 1124
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Python Brain", "UI / React"]
entities: ["M0001"]
---

# Source Card — M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX.md

## Source

[[docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX|docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX.md]]

## Summary

The Python node price is the truth. The visual marker must point exactly to it. Wingdings arrow glyphs in MT5 can have confusing visual centers/anchors. To avoid glyph-anchor ambiguity, the default node marker is now a custom two-segment chevron: HIGH node: red `V` marker, exact vertex at node high, wings above the candle LOW node: green `^` marker, exact vertex at node low, wings below the candle Inputs: The exact chevron vertex is the Python node price. The bridge previously rewrote the runtime config on every timer cycle. That can cause Python to recompute the same candle stream repeatedly. Now the timer does not rewrite config unless explicitly requested: Normal flow:

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

M0001

## Headings

- M0001 Node Marker Precision and Bridge Performance Fix
  - Node marker
  - Performance

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `12`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `12`
- [[docs/M0001_NODE_ARROW_TIP_ANCHOR_FIX|M0001_NODE_ARROW_TIP_ANCHOR_FIX.md]] — score `12`
- [[docs/M0001_PARQUET_TYPE_SAFETY_FIX|M0001_PARQUET_TYPE_SAFETY_FIX.md]] — score `12`
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
