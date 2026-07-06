
---
type: source_card
source_path: "docs/mql_native/M0001_CONSUMED_NODE_REPAIR.md"
source_ext: ".md"
source_size: 849
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_CONSUMED_NODE_REPAIR.md

## Source

[[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|docs/mql_native/M0001_CONSUMED_NODE_REPAIR.md]]

## Summary

Once a node is consumed/hunted, its job is finished. For a consumed node: The expansion extreme is a live decision variable only while the node is still active. `DAL_M0001ComputeNodeAuditStates()` now stops scanning a node immediately when it is consumed/hunted. It does not continue updating the expansion extreme after the consume candle. Active nodes can show: Consumed nodes show only an optional marker: The structural node remains on the chart for audit history, but the active extreme and live hunt zone disappear after consumption. Version: `1.22`.

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Consumed Node Repair
  - Rule
  - Engine change
  - Visual change
  - Important

## Related Source Documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `16`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `16`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001_FAST_FINAL_ONLY_RUNTIME.md]] — score `16`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md]] — score `16`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `16`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `16`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `16`
- [[docs/debug/E0006/README|README.md]] — score `15`
- [[docs/debug/E0006_ALL_ZONE_TOUCH_LIMIT_README|E0006_ALL_ZONE_TOUCH_LIMIT_README.md]] — score `15`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
