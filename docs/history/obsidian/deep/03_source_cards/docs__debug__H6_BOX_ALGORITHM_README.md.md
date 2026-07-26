
---
type: source_card
source_path: "docs/debug/H6_BOX_ALGORITHM_README.md"
source_ext: ".md"
source_size: 5225
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — H6_BOX_ALGORITHM_README.md

## Source

[[docs/debug/H6_BOX_ALGORITHM_README|docs/debug/H6_BOX_ALGORITHM_README.md]]

## Summary

H6 does not compute touch, extreme, zone, revisit, or invalidation. It uses M0001 only: `DAL_DetectLRuleNodes` `DAL_M0001ComputeEvents` `event.territory_lower` `event.territory_upper` `event.entry_index` `event.exit_index` `event.touch_confirmed` By default, every confirmed M0001 event gets exactly one persistent box. This is intentionally broader than the old horizon-only logic so no touched/revisited event disappears just because it is below H1. Box vertical bounds are exactly M0001 territory: H6 does not rebuild zone geometry. Default: `InpH6BoxRightMode`: `0`: right edge = horizon candle `1`: right edge = M0001 event exit candle `2`: right edge = latest available bar Touch candle is zero. Age is: Color: Boxes use this prefix: Live updates never delete boxes. Lifecycle is upsert-only: H6 runs: once on init for backfill once per new candle for live update It never runs per tick. No hea

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- H6 Fast Box Visualizer — Official Algorithm
  - Source of truth
  - What gets drawn
  - Geometry
  - Time range
  - Color
  - Persistence
  - Execution
  - Performance
  - Release 141 — selectable zone projection mode
    - `DAL_M0006_ZONE_FULL_M0001_TERRITORY`
    - `DAL_M0006_ZONE_NODE_CAPPED_90_TO_NODE`

## Related Source Documents

- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `16`
- [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md]] — score `16`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `16`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `16`
- [[docs/architecture|architecture.md]] — score `15`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `15`
- [[docs/debug/E0006/README|README.md]] — score `15`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `15`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `15`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
