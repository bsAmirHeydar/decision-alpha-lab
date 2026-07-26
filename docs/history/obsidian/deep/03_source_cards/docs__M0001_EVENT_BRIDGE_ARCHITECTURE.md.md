
---
type: source_card
source_path: "docs/M0001_EVENT_BRIDGE_ARCHITECTURE.md"
source_ext: ".md"
source_size: 3039
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_EVENT_BRIDGE_ARCHITECTURE.md

## Source

[[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|docs/M0001_EVENT_BRIDGE_ARCHITECTURE.md]]

## Summary

M0001 must be live-like without creating two brains. The tested implementation, the research implementation, and the chart-inspected implementation must be the same Python code. MQL is not allowed to compute M0001. It only: exports market candles observed by MT5; writes input parameters; draws Python output; can later execute orders from Python decisions. The previous bridge only let MQL write parameters. Python still read cached candles. That was useful for research, but it did not feel synchronized with the visual chart. The event bridge uses the chart as the market-data trigger. When a new candle arrives, or optionally every tick, MQL sends the current candle stream to Python. Recommended research mode: This is live-safe because the forming candle is excluded. Tick-inspection mode: This updates faster, but the current candle can change. Use it for visual inspection, not final non-repa

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Event Bridge Architecture
  - Goal
  - Architecture
  - Why this is different from the old bridge
  - Important MQL inputs
  - Python watcher
  - Sync files
  - Validation rule

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `26`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `19`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `19`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `19`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `18`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `18`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `18`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL_NATIVE_MIGRATION_DECISION.md]] — score `18`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `18`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
