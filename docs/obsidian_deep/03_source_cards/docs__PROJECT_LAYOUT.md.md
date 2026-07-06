
---
type: source_card
source_path: "docs/PROJECT_LAYOUT.md"
source_ext: ".md"
source_size: 1279
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "MQL Native"]
entities: []
---

# Source Card — PROJECT_LAYOUT.md

## Source

[[docs/PROJECT_LAYOUT|docs/PROJECT_LAYOUT.md]]

## Summary

This repository has one canonical root: The repository must **not** contain another tracked project copy under: All execution code, include files, and execution documentation must be edited in the canonical root paths above. A nested `decision-alpha-lab/` directory creates two competing source trees. That causes: patch context drift; MetaEditor compiling one copy while Git shows changes in another copy; duplicate include paths; stale execution modules surviving after a release update; false confidence that a fix was applied when the terminal is still reading the old file. If a nested project copy exists, back it up once, remove it, and commit the deletion: The backup zip is a temporary safety artifact and should not be committed.

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

—

## Headings

- Decision Alpha Lab project layout
  - Canonical source paths
  - Why nested project copies are banned
  - Cleanup rule

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `5`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015_cme_live_backtest_plan.md]] — score `5`
- [[docs/laboratory_architecture|laboratory_architecture.md]] — score `5`
- [[docs/M0001_COMMON_FILES_SYNC_FIX|M0001_COMMON_FILES_SYNC_FIX.md]] — score `5`
- [[docs/M0001_EVENT_BRIDGE_ARCHITECTURE|M0001_EVENT_BRIDGE_ARCHITECTURE.md]] — score `5`
- [[docs/M0001_MQL_INPUT_PARAMETER_BRIDGE|M0001_MQL_INPUT_PARAMETER_BRIDGE.md]] — score `5`
- [[docs/M0001_PARQUET_EVENT_BRIDGE|M0001_PARQUET_EVENT_BRIDGE.md]] — score `5`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `5`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `5`
- [[docs/mql_live_visual_lab|mql_live_visual_lab.md]] — score `5`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
