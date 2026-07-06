
---
type: source_card
source_path: "tools/astro_validation/README_pure_entry_excel.md"
source_ext: ".md"
source_size: 1090
empty: false
generated_at: 2026-07-06
concepts: ["Astro ML", "Execution / Risk", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — README_pure_entry_excel.md

## Source

[[tools/astro_validation/README_pure_entry_excel|tools/astro_validation/README_pure_entry_excel.md]]

## Summary

Builds a fast batch Excel report from an astro feature CSV without running MT5 ticks. Output workbook sheets: `RunSummary`: run metadata and counts `EntryWindows`: one row per complete `enter_long` / `enter_short` window `EntryBars`: every bar belonging to those full entry windows `ExitEvents`: first exit warning and resolved paper-exit event per entry window Default output location for the PowerShell helper: `%APPDATA%\MetaQuotes\Terminal\Common\Files\astro\reports\nas100_pure_entry_windows.xlsx` Quick command from the project root: Or use the helper:

## Concepts

[[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Pure Astro Entry Excel Report

## Related Source Documents

- [metadata.yaml](../../lab/03_experiments/EXP0013_astro_feature_store/metadata.yaml) — score `16`
- [metadata.yaml](../../lab/03_experiments/EXP0016_astro_meta_learner/metadata.yaml) — score `14`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [metadata.yaml](../../lab/03_experiments/EXP0012_distributional_cluster_miner/metadata.yaml) — score `12`
- [metadata.yaml](../../lab/03_experiments/EXP_flag_counting/metadata.yaml) — score `12`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `12`
- [[tools/astro_validation/README|README.md]] — score `11`
- [[docs/architecture|architecture.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
