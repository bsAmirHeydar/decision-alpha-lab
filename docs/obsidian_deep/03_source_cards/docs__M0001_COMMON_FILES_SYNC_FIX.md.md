
---
type: source_card
source_path: "docs/M0001_COMMON_FILES_SYNC_FIX.md"
source_ext: ".md"
source_size: 1539
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "MQL Native", "Python Brain", "UI / React"]
entities: ["M0001"]
---

# Source Card — M0001_COMMON_FILES_SYNC_FIX.md

## Source

[[docs/M0001_COMMON_FILES_SYNC_FIX|docs/M0001_COMMON_FILES_SYNC_FIX.md]]

## Summary

When the Expert is attached in MT5, MQL can write files into a different sandbox than the Python watcher is reading from, especially in Strategy Tester / Visual Mode. Typical symptom: The EA may actually be writing into tester/local file storage, not the same folder watched by Python. Use MetaQuotes Common Files as the bridge root. MQL input: Python watcher default: Shared root: Bridge files: Attach and compile: Set: Run Python: The PowerShell output should now watch:

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

M0001

## Headings

- M0001 Common Files Sync Fix
  - Problem
  - Fix
  - Run

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `14`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `14`
- [[docs/M0001_PARQUET_EVENT_BRIDGE|M0001_PARQUET_EVENT_BRIDGE.md]] — score `14`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `14`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL_NATIVE_MIGRATION_DECISION.md]] — score `14`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `14`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `13`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `13`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `13`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `13`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
