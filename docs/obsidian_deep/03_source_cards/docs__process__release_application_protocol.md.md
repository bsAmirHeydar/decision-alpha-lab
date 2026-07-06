
---
type: source_card
source_path: "docs/process/release_application_protocol.md"
source_ext: ".md"
source_size: 1770
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "MQL Native"]
entities: []
---

# Source Card — release_application_protocol.md

## Source

[[docs/process/release_application_protocol|docs/process/release_application_protocol.md]]

## Summary

This document standardizes how release ZIP/PATCH files should be applied in the project. Apply commands should be short and should clean their own release files. They should not include `git status` by default. Only use this if the ZIP has not already been applied. Commit only project files: source files, include files, documentation, registry updates, lab reports. Do not commit: release ZIP files, release PATCH files, installer scripts, temporary backups, generated logs unless explicitly intended. After MQL5 changes: close MetaEditor, apply release, run installer if it syncs terminal-level includes, reopen MetaEditor, compile the changed Experts, only then commit. MetaEditor may read terminal-level includes from: while the repo may keep source includes in: Installers should sync include files when necessary.

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

—

## Headings

- Release Application Protocol
  - User-facing rule
  - ZIP apply block
  - PATCH apply block
  - Commit rule
  - MetaEditor rule
  - Include sync rule

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `10`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `10`
- [[lab/03_experiments/EXP0000_sample/report|report.md]] — score `8`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|report.md]] — score `8`
- [[lab/05_validation/VAL001/report|report.md]] — score `8`
- [[docs/process/metatrader_compile_checklist|metatrader_compile_checklist.md]] — score `5`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `4`
- [[docs/architecture|architecture.md]] — score `4`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
