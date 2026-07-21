
---
type: source_card
source_path: "docs/mql_native/M0001_LIVE_ZONE_RESYNC.md"
source_ext: ".md"
source_size: 1346
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "UI / React", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_LIVE_ZONE_RESYNC.md

## Source

[[docs/mql_native/M0001_LIVE_ZONE_RESYNC|docs/mql_native/M0001_LIVE_ZONE_RESYNC.md]]

## Summary

The visible zone box must not freeze while the node is still alive. Pending-touch/event geometry is intentionally frozen for exit-gap confirmation, but the active live zone should continue to follow the latest expansion extreme. For every alive node: The pending event zone remains frozen internally for touch confirmation only: After a confirmed revisit in HUNT mode: So the current live box does not stretch from the original node origin after a confirmed revisit. `DAL_DrawRectangle` now upserts geometry. If a rectangle already exists, both anchor points are moved explicitly: This prevents stale rectangle coordinates if the same object name is reused. `M0001_LiveVisualLab.mq5` version: `1.45`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Live Zone Resync
  - Problem
  - Fix
  - Revisit cycles
  - Renderer safety
  - Version

## Related Source Documents

- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `16`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `16`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `16`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `16`
- [[docs/mql_native/M0001_REVISIT_EXTREME_RESET|M0001_REVISIT_EXTREME_RESET.md]] — score `16`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `16`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `16`
- [[docs/mql_native/MQL_NATIVE_ARCHITECTURE|MQL_NATIVE_ARCHITECTURE.md]] — score `16`
- [[docs/architecture|architecture.md]] — score `15`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
