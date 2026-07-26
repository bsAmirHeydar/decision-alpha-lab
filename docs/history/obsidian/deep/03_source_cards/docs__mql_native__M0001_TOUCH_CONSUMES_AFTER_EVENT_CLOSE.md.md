
---
type: source_card
source_path: "docs/mql_native/M0001_TOUCH_CONSUMES_AFTER_EVENT_CLOSE.md"
source_ext: ".md"
source_size: 1220
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_TOUCH_CONSUMES_AFTER_EVENT_CLOSE.md

## Source

[[docs/mql_native/M0001_TOUCH_CONSUMES_AFTER_EVENT_CLOSE|docs/mql_native/M0001_TOUCH_CONSUMES_AFTER_EVENT_CLOSE.md]]

## Summary

Touch mode now follows the README semantics: Touch does **not** consume the node immediately. An event is complete when price has stayed outside the frozen event territory for `exit_gap` consecutive candles. When the first touch starts an event: These are frozen for the event. They are not updated while the event is active. Hunt mode remains separate: Zone touches in hunt mode start/revisit events, but do not consume the node unless the node price is broken. This preserves revisit semantics: `M0001_LiveVisualLab.mq5` version: `1.30`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Touch Mode: Consume After Event Completion
  - Decision
  - Event completion
  - Frozen event geometry
  - HUNT mode
  - Why this matters
  - Version

## Related Source Documents

- [[docs/debug/E0006/README|README.md]] — score `21`
- [[docs/execution/README|README.md]] — score `21`
- [[docs/ui/README|README.md]] — score `21`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|README.md]] — score `21`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `21`
- [[README|README.md]] — score `21`
- [[docs/debug/E0008/README|README.md]] — score `19`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|README.md]] — score `19`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `19`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|README.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
