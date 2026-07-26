
---
type: source_card
source_path: "docs/M0001_PARQUET_EVENT_BRIDGE.md"
source_ext: ".md"
source_size: 2150
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_PARQUET_EVENT_BRIDGE.md

## Source

[[docs/M0001_PARQUET_EVENT_BRIDGE|docs/M0001_PARQUET_EVENT_BRIDGE.md]]

## Summary

The M0001 research brain must stay in Python, and all durable research artifacts should be stored as Parquet. MQL5 cannot read or write Parquet natively without external DLLs. Therefore the architecture is: The CSV render adapter is not the research artifact. It exists only because MQL can read simple text files natively. Python writes these on every bridge cycle: These are the files to use for: research replay validation journal Python/MQL visual audit reproducibility future reports strategy decision logs MQL still consumes: This file is only a drawing contract. It should not be used as the source of truth. Attach the Expert: Recommended MQL inputs: Then run the Python watcher: The status panel shows: If the chart says it is waiting for the Python visual contract, the watcher is not running or has not produced the adapter file yet. Check the PowerShell output and the status file.

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Parquet Event Bridge
  - Why
  - Authoritative Parquet artifacts
  - MQL render adapter
  - Run
  - Status

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `26`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `23`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `19`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `19`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `18`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `18`
- [[docs/MQL_NATIVE_MIGRATION_DECISION|MQL_NATIVE_MIGRATION_DECISION.md]] — score `18`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `18`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `18`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
