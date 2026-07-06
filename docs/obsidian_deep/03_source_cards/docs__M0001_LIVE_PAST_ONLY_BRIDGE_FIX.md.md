
---
type: source_card
source_path: "docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX.md"
source_ext: ".md"
source_size: 1090
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Python Brain"]
entities: ["M0001"]
---

# Source Card — M0001_LIVE_PAST_ONLY_BRIDGE_FIX.md

## Source

[[docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX|docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX.md]]

## Summary

Strategy Tester could show nodes from future candles if the bridge exported a count-based historical window rather than a time-bounded window. MQL repeatedly deleted and redrew objects on every timer, causing flicker and overload. Python could hit `PermissionError [WinError 32]` while refreshing the MQL CSV adapter while MT5 was reading it. MQL exports candles using a time-bounded `CopyRates(start_time, end_time)` call. `end_time` is the last closed bar when `InpBridgeClosedBarsOnly=true`. MQL redraws only when Python publishes a new `request_id` in the status file. MQL file handles use share flags. Python writes the visual adapter through a temp file and retries on Windows file locks. This is the closest live-safe visual mode: only information available up to the current simulated closed candle is exported to Python.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]

## Entities

M0001

## Headings

- M0001 Live Past-Only Event Bridge Fix
  - Problems
  - Fixes
  - Important inputs

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `10`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001_EVENT_BRIDGE_ARCHITECTURE.md]] — score `10`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `10`
- [[docs/M0001_NODE_ARROW_TIP_ANCHOR_FIX|M0001_NODE_ARROW_TIP_ANCHOR_FIX.md]] — score `10`
- [[docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX|M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX.md]] — score `10`
- [[docs/M0001_NODE_REVEAL_TIMING_FIX|M0001_NODE_REVEAL_TIMING_FIX.md]] — score `10`
- [[docs/M0001_PARQUET_TYPE_SAFETY_FIX|M0001_PARQUET_TYPE_SAFETY_FIX.md]] — score `10`
- [[docs/M0001_REVERT_NODE_TIMING_FAST_SYNC|M0001_REVERT_NODE_TIMING_FAST_SYNC.md]] — score `10`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `10`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
