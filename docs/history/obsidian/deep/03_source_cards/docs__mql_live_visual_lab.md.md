
---
type: source_card
source_path: "docs/mql_live_visual_lab.md"
source_ext: ".md"
source_size: 1488
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — mql_live_visual_lab.md

## Source

[[docs/mql_live_visual_lab|docs/mql_live_visual_lab.md]]

## Summary

MQL5 is now a visual-only layer. The metric brain is Python: The MT5 expert reads the Python-generated CSV visual contract: and draws it on the chart. Despite the name `LiveVisualLab`, the expert does not compute live logic. It reloads the Python visual contract on a timer and redraws it. This keeps research, tests, backtest artifacts and live visual inspection on one… Compile: Attach it to the same symbol/timeframe chart and set: All manual visual toggles are false by default. Use presets or turn on layers one by one.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- MQL5 Visual Lab: Python Brain, MT5 Eyes
  - Main expert
  - Run Python brain once
  - Run Python brain continuously
  - Compile and attach MQL
  - Read more

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `24`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `24`
- [[docs/mql_live_visual_lab_debug_packages|mql_live_visual_lab_debug_packages.md]] — score `22`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001_EVENT_BRIDGE_ARCHITECTURE.md]] — score `16`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `16`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `16`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL_NATIVE_MIGRATION_DECISION.md]] — score `16`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `16`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `16`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
