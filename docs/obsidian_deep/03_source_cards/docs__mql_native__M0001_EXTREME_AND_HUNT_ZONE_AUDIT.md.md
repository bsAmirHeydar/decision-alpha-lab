
---
type: source_card
source_path: "docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT.md"
source_ext: ".md"
source_size: 1285
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "MQL Native", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_EXTREME_AND_HUNT_ZONE_AUDIT.md

## Source

[[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT.md]]

## Summary

After validating L-rule structural nodes, the next audit layer is expansion state: For LOW nodes: For HIGH nodes: The visual layer draws a dashed line: The live hunt zone is the current territory rectangle computed from the distance between the node price and the tracked expansion extreme. If the node has not been invalidated/hunted, the rectangle extends from `active_from_time` to the current live-stream bar. If the node is invalidated and `InpShowInvalidatedHuntZones=false`, no rectangle is drawn for it. The L-rule node detector is now exposed through: Downstream M0001 modules should use this stable facade and avoid modifying the validated detector internals.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Extreme and Live Hunt Zone Audit
  - Purpose
  - Inputs
  - Expansion extreme
  - Live hunt zone
  - Structural node module boundary

## Related Source Documents

- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `14`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `14`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `14`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `14`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md]] — score `14`
- [[docs/mql_native/M0001_HUNT_ZONE_FROM_NODE_ORIGIN|M0001_HUNT_ZONE_FROM_NODE_ORIGIN.md]] — score `14`
- [[docs/evidence/m0001_json_audit/2e8468dd6e0a_M0001_JSON_AUDIT_REPORT|M0001_JSON_AUDIT_REPORT.md]] — score `14`
- [[docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON|M0001_LOGRTV_RANDOM_NULL_COMPARISON.md]] — score `14`
- [[docs/mql_native/M0001_MINIMAL_INPUTS|M0001_MINIMAL_INPUTS.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
