---
title: "Pure Astro Entry Excel Report"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "tools/astro_validation/README_pure_entry_excel.md"
source_ext: ".md"
category: "tool_docs"
source_size_bytes: "1090"
concepts:
  - "Astro ML"
  - "Execution"
  - "Validation"
---


# Pure Astro Entry Excel Report

**Source:** [[tools/astro_validation/README_pure_entry_excel|tools/astro_validation/README_pure_entry_excel.md]]

**Category:** `tool_docs`  
**Status:** ok  
**Size:** `1090` bytes

## خلاصه

Builds a fast batch Excel report from an astro feature CSV without running MT5 ticks. Output workbook sheets: `RunSummary`: run metadata and counts `EntryWindows`: one row per complete `enter_long` / `enter_short` window `EntryBars`: every bar belonging to those full entry windows `ExitEvents`: first exit warning and resolved paper-exit event per entry window Default output location for the PowerShell helper: `%APPDATA%\MetaQuotes\Terminal\Common\Files\astro\reports\nas100_pure_entry_windows.xlsx` Quick command from the project root: Or use the helper:

## Headings

- Pure Astro Entry Excel Report

## Concepts

- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[tools/astro_validation/README|Astro Signal Validator]] — `tool_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/finalization/README|EXP0013 Finalization Snapshot]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[mql5/Experts/AstroExecution/README|Astro Execution]] — `mql5_docs`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`
- [[tools/astro_feature_builder/README|Astro Feature Builder]] — `tool_docs`
- [[tools/astro_live_bridge/README|EXP0013 Astro Live Bridge V2]] — `tool_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
