
---
type: source_card
source_path: "docs/evidence/val_m0001_mql_native/454e81f9f0b3_report.md"
source_ext: ".md"
source_size: 504
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — report.md

## Source

[[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|docs/evidence/val_m0001_mql_native/454e81f9f0b3_report.md]]

## Summary

Visual and journal validation for the native MQL5 implementation of M0001. [ ] L-rule high node confirms exactly at `i + L`. [ ] L-rule low node confirms exactly at `i + L`. [ ] Marker is drawn on pivot candle. [ ] Active-from line, when enabled, is drawn at `i + L`. [ ] Event scan does not start before active-from. [ ] RTV fields match the event window and before-window lengths. [ ] Strategy Tester visual state does not require Python.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- VAL_M0001_MQL_NATIVE
  - Scope
  - Checklist

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `17`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `17`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `17`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `17`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `17`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `17`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `17`
- [[docs/mql_native/MQL_NATIVE_ARCHITECTURE|MQL_NATIVE_ARCHITECTURE.md]] — score `17`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL_NATIVE_MIGRATION_DECISION.md]] — score `17`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
