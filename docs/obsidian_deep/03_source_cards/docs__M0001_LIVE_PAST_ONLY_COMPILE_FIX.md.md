
---
type: source_card
source_path: "docs/M0001_LIVE_PAST_ONLY_COMPILE_FIX.md"
source_ext: ".md"
source_size: 577
empty: false
generated_at: 2026-07-06
concepts: []
entities: ["M0001"]
---

# Source Card — M0001_LIVE_PAST_ONLY_COMPILE_FIX.md

## Source

[[docs/M0001_LIVE_PAST_ONLY_COMPILE_FIX|docs/M0001_LIVE_PAST_ONLY_COMPILE_FIX.md]]

## Summary

The previous live past-only bridge snapshot accidentally inserted the `StatusValue` helper as escaped text (`\n`) on one physical MQL line. MetaEditor then parsed the whole block as invalid global tokens. Typical compile errors: `StatusValue()` is now emitted as normal MQL source code. The missing input `InpBridgeTimerConfigPulse` is also declared. Version: `6.51`.

## Concepts

—

## Entities

M0001

## Headings

- M0001 Live Past-Only Bridge Compile Fix
  - Problem
  - Fix

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `6`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `6`
- [[docs/M0001_COMMON_FILES_SYNC_FIX|M0001_COMMON_FILES_SYNC_FIX.md]] — score `6`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001_EVENT_BRIDGE_ARCHITECTURE.md]] — score `6`
- [[docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX|M0001_LIVE_PAST_ONLY_BRIDGE_FIX.md]] — score `6`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `6`
- [[docs/M0001_NODE_ARROW_TIP_ANCHOR_FIX|M0001_NODE_ARROW_TIP_ANCHOR_FIX.md]] — score `6`
- [[docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX|M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX.md]] — score `6`
- [[docs/M0001_NODE_REVEAL_TIMING_FIX|M0001_NODE_REVEAL_TIMING_FIX.md]] — score `6`
- [[docs/M0001_PARQUET_EVENT_BRIDGE|M0001_PARQUET_EVENT_BRIDGE.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
