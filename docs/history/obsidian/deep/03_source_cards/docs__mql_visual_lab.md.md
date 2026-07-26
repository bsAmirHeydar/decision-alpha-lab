
---
type: source_card
source_path: "docs/mql_visual_lab.md"
source_ext: ".md"
source_size: 2631
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — mql_visual_lab.md

## Source

[[docs/mql_visual_lab|docs/mql_visual_lab.md]]

## Summary

The React/FastAPI UI has been removed. The project now uses a cleaner split: M0001 is computed in Python from the same live-style candle-by-candle engine for: actual L-rule structural nodes random baseline reference points Python exports a simple CSV visual contract. MQL5 reads the CSV and draws objects directly on the MT5 chart. From the project root: With random baseline: Default output: Copy that CSV to your real terminal data folder: Copy the expert: to: Then compile it in MetaEditor and attach it to the same symbol/timeframe chart. The MQL expert has inputs for toggling: The research truth stays in Python, where it is testable and reproducible. The visual inspection happens in MT5/MQL5, where the chart, market context and execution feeling are native. A second expert exists for live / Strategy Tester style inspection: This expert does not read the Python CSV. It computes L-rule node

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- MQL5 Visual Lab Architecture
  - Core idea
  - Main files
  - Export example
  - Visual layers
  - Why this is cleaner
  - Live visual testing mode

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `30`
- [[docs/mql_live_visual_lab|mql_live_visual_lab.md]] — score `24`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `22`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `21`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `20`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `20`
- [[docs/mql_live_visual_lab_debug_packages|mql_live_visual_lab_debug_packages.md]] — score `20`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL_NATIVE_MIGRATION_DECISION.md]] — score `20`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `20`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
