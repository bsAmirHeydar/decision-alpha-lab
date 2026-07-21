
---
type: source_card
source_path: "docs/mql_native/MQL_NATIVE_ARCHITECTURE.md"
source_ext: ".md"
source_size: 1909
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — MQL_NATIVE_ARCHITECTURE.md

## Source

[[docs/mql_native/MQL_NATIVE_ARCHITECTURE|docs/mql_native/MQL_NATIVE_ARCHITECTURE.md]]

## Summary

Version: 1.59 The active runtime is MQL5-native. Python, FastAPI, React, Parquet caches, CSV bridges, Excel/JSON report generation, and external watcher loops are not part of the active execution path. Fast final-only mode: Visual replay mode: MQL5 is the source of truth for: candle access, warmup historical seeding, L-rule structural node detection, M0001 territory/event construction, HUNT/TOUCH/revisit semantics, RTV/logRTV calculation, matched random baseline, final chart visualization. The canonical active semantics are documented in:

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- MQL-Native Runtime Architecture
  - Decision
  - Active runtime flow
  - Source of truth
  - Active module layout
  - Removed from active runtime
  - Logic lock

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `27`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `25`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md]] — score `24`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|report.md]] — score `21`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `21`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `20`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `20`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `20`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `20`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
