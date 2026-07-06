
---
type: source_card
source_path: "docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md"
source_ext: ".md"
source_size: 4318
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Intermarket Divergence", "MQL Native", "Python Brain", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md

## Source

[[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]]

## Summary

M0001 has one brain only: The MQL expert does not compute nodes, territories, events, RTV, hunts, random baselines, or validation logic. It reads the visual contract produced by Python and draws it on the MT5 chart. The lab is intentionally designed around one obsessive rule: There must not be a separate MQL implementation of the metric and a separate Python implementation of the metric. Two engines create a hidden risk: the visual chart can look correct while the research engine is different… The same Python modules are used by every mode: These modules feed: MQL is allowed to: MQL is not allowed to: The live behavior is produced by repeatedly running the Python engine on the latest available candle window and exporting the visual contract. MT5 reloads that contract on a timer. This gives the live/testing feel while preserving single-source correctness: The MQL expert supports visual pa

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Single-Source Live Architecture
  - Core decision
  - Why this matters
  - Runtime flow
  - Single-source invariant
  - What MQL is allowed to do
  - Live-like behavior without two engines
  - Debug packages
  - Validation philosophy
  - Professional framing
  - Anti-pattern avoided

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `28`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `20`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `20`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `19`
- [[README_M0001_PYTHON_BRAIN_MQL_VISUAL|README_M0001_PYTHON_BRAIN_MQL_VISUAL.md]] — score `19`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001_EVENT_BRIDGE_ARCHITECTURE.md]] — score `18`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `18`
- [[docs/mql_live_visual_lab_debug_packages|mql_live_visual_lab_debug_packages.md]] — score `18`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL_NATIVE_MIGRATION_DECISION.md]] — score `18`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
