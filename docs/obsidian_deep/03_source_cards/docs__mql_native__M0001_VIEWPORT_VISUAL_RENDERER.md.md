
---
type: source_card
source_path: "docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER.md"
source_ext: ".md"
source_size: 1219
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "MQL Native", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_VIEWPORT_VISUAL_RENDERER.md

## Source

[[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER.md]]

## Summary

The M0001 engine can compute hundreds of nodes and audit states. Drawing every node, every price label, every consumed marker, every extreme line, and every hunt-zone rectangle on one MT5 chart can overload chart-object rendering. This can look like nodes stop appearing after a point even though the detector is still computing them. The renderer now defaults to viewport-based drawing: The engine still computes all data. The chart only draws objects whose time range intersects the currently visible chart window plus padding. When the chart is scrolled or zoomed, `OnChartEvent(CHARTEVENT_CHART_CHANGE)` redraws the objects for the new viewport. This is not a research/data limit. still means all tester/history bars. Viewport rendering only limits the number of chart objects created at once, so MT5 does not choke on thousands of objects. With diagnostics enabled, the summary shows: `M0001_Liv

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Viewport Visual Renderer
  - Problem
  - Fix
  - Important distinction
  - Summary
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `18`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `18`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `18`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001_MINIMAL_INPUTS.md]] — score `18`
- [[docs/mql_native/M0001_RTV_LOG_HILO|M0001_RTV_LOG_HILO.md]] — score `18`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `18`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `18`
- [[docs/architecture|architecture.md]] — score `17`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `17`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
