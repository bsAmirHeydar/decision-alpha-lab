
---
type: source_card
source_path: "docs/M0001_VISUAL_TOGGLE_SYNC_FIX.md"
source_ext: ".md"
source_size: 1055
empty: false
generated_at: 2026-07-06
concepts: []
entities: ["M0001"]
---

# Source Card — M0001_VISUAL_TOGGLE_SYNC_FIX.md

## Source

[[docs/M0001_VISUAL_TOGGLE_SYNC_FIX|docs/M0001_VISUAL_TOGGLE_SYNC_FIX.md]]

## Summary

The chart can still show objects after manual visual toggles are set to `false` when: `InpViewPreset` is not `0`; presets intentionally turn layers on. Old objects from previous prefixes remain on the chart. Strategy Tester keeps drawing previous objects until the EA deletes them. The Expert now has hard visual controls: Recommended blank chart: Recommended manual/custom mode: Preset mode: Manual toggles are only fully manual when: or: If `InpViewPreset` is 10, 11, or 12, it will draw preset layers even when the individual toggles are false.

## Concepts

—

## Entities

M0001

## Headings

- M0001 Visual Toggle Sync Fix
  - Problem
  - Fix
  - Important rule

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `6`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `6`
- [[docs/M0001_COMMON_FILES_SYNC_FIX|M0001_COMMON_FILES_SYNC_FIX.md]] — score `6`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001_EVENT_BRIDGE_ARCHITECTURE.md]] — score `6`
- [[docs/M0001_LIVE_PAST_ONLY_BRIDGE_FIX|M0001_LIVE_PAST_ONLY_BRIDGE_FIX.md]] — score `6`
- [[docs/M0001_LIVE_PAST_ONLY_COMPILE_FIX|M0001_LIVE_PAST_ONLY_COMPILE_FIX.md]] — score `6`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `6`
- [[docs/M0001_NODE_ARROW_TIP_ANCHOR_FIX|M0001_NODE_ARROW_TIP_ANCHOR_FIX.md]] — score `6`
- [[docs/M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX|M0001_NODE_MARKER_PRECISION_AND_PERFORMANCE_FIX.md]] — score `6`
- [[docs/M0001_NODE_REVEAL_TIMING_FIX|M0001_NODE_REVEAL_TIMING_FIX.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
