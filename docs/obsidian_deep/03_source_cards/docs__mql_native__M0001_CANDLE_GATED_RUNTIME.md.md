
---
type: source_card
source_path: "docs/mql_native/M0001_CANDLE_GATED_RUNTIME.md"
source_ext: ".md"
source_size: 1496
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_CANDLE_GATED_RUNTIME.md

## Source

[[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|docs/mql_native/M0001_CANDLE_GATED_RUNTIME.md]]

## Summary

Version: 1.59 M0001 is still an Expert Advisor, so MetaTrader wakes it through `OnTick()`. The research engine itself is not tick-based. The timer is disabled by default: If a timer is enabled later, it must pass through the same candle gate. The optimized default is: This keeps runtime light while restoring final chart drawings. During the run the EA appends closed candles only. At shutdown, the same final computed state is used for both: `DAL_M0001_FINAL_NODES` / `DAL_M0001_FINAL_RANDOM` final node, zone, revisit, state, and optional RTV/event drawings For step-by-step visual debugging: This recomputes and redraws on each newly closed candle only. It never runs heavy logic on intra-candle ticks, but it is intentionally slower than final-only mode. The candle gate does not change: structural-node definition, `active_from = node_index + L`, territory formula, HUNT priority, exit-gap conf

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Candle-Gated Runtime
  - Runtime behavior
  - Fast default
  - Visual replay mode
  - Semantics unchanged

## Related Source Documents

- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `20`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `20`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001_EVENT_BRIDGE_ARCHITECTURE.md]] — score `19`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `18`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `18`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `18`
- [[docs/mql_native/MQL_NATIVE_ARCHITECTURE|MQL_NATIVE_ARCHITECTURE.md]] — score `18`
- [[docs/architecture|architecture.md]] — score `17`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `17`
- [[docs/debug/E0006/README|README.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
