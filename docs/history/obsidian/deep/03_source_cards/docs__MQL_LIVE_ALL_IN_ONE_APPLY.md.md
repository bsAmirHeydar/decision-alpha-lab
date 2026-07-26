
---
type: source_card
source_path: "docs/MQL_LIVE_ALL_IN_ONE_APPLY.md"
source_ext: ".md"
source_size: 1326
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — MQL_LIVE_ALL_IN_ONE_APPLY.md

## Source

[[docs/MQL_LIVE_ALL_IN_ONE_APPLY|docs/MQL_LIVE_ALL_IN_ONE_APPLY.md]]

## Summary

This snapshot is the combined architecture change: removes the old React/FastAPI UI stack from the working tree keeps the Python research engine adds the modular M0001 RTV engine keeps the Python-to-MQL CSV exporter for audit/static visualization adds the MQL5 static CSV visualizer adds the MQL5 live visual tester that computes RTV directly in MT5 From the project root: Then compile in MetaEditor: Python remains the reproducible research engine: It can compute actual L-rule nodes and random baselines with the same metric logic. This expert computes from currently available MT5 bars: L-rule nodes node confirmation delay territories events RTV hunt markers currently open event labels Use `InpUseClosedBarsOnly=true` and `InpUpdateOnEveryTick=false` for live-safe bar-by-bar testing.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- MQL Live Visual Lab — All-in-One Apply
  - One-shot apply
  - What stays in Python
  - What runs live in MQL

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `30`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `22`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `21`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `20`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `20`
- [[docs/mql_live_visual_lab_debug_packages|mql_live_visual_lab_debug_packages.md]] — score `20`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL_NATIVE_MIGRATION_DECISION.md]] — score `20`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `20`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `19`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
