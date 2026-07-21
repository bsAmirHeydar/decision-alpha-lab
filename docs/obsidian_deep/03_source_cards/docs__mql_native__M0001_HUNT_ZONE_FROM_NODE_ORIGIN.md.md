
---
type: source_card
source_path: "docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN.md"
source_ext: ".md"
source_size: 990
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "MQL Native", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_HUNT_ZONE_FROM_NODE_ORIGIN.md

## Source

[[docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN|docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN.md]]

## Summary

Live hunt/territory rectangles now start from the original structural node time, not from `active_from_time`. Before: Now: The rectangle still extends to: or, for invalidated nodes when enabled: The visual audit should show the full territory relationship from the node origin. The node itself remains the structural anchor, while `active_from_time` remains the live-safe confirmation point used by the logic. This is a visual-origin change only. The detector still confirms nodes using the L-rule: The M0001 logic still uses confirmed nodes only. The rectangle simply begins at the node candle to make the territory's structural origin visually clear. `M0001_LiveVisualLab.mq5` version: `1.21`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Hunt Zone Origin From Node
  - Change
  - Why
  - Important
  - Version

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `14`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `14`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `14`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `14`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|M0001_EXTREME_AND_HUNT_ZONE_AUDIT.md]] — score `14`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md]] — score `14`
- [[docs/evidence/m0001_json_audit/2e8468dd6e0a_M0001_JSON_AUDIT_REPORT|M0001_JSON_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON|M0001_LOGRTV_RANDOM_NULL_COMPARISON.md]] — score `14`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001_MINIMAL_INPUTS.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
