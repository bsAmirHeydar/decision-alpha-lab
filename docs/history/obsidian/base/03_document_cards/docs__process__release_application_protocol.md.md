---
title: "Release Application Protocol"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/process/release_application_protocol.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "1770"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
---


# Release Application Protocol

**Source:** [[docs/process/release_application_protocol|docs/process/release_application_protocol.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `1770` bytes

## خلاصه

This document standardizes how release ZIP/PATCH files should be applied in the project. Apply commands should be short and should clean their own release files. They should not include `git status` by default. Only use this if the ZIP has not already been applied. Commit only project files: source files, include files, documentation, registry updates, lab reports. Do not commit: release ZIP files, release PATCH files, installer scripts, temporary backups, generated logs unless explicitly intended. After MQL5 changes: 1. close MetaEditor, 2. apply release, 3. run installer if it syncs terminal-level includes, 4. reopen MetaEditor, 5. compile the changed Experts, 6. only then commit. MetaEdit

## Headings

- Release Application Protocol
-   User-facing rule
-   ZIP apply block
-   PATCH apply block
-   Commit rule
-   MetaEditor rule
-   Include sync rule

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/process/metatrader_compile_checklist|MetaTrader Compile Checklist]] — `core_docs`
- [[lab/03_experiments/EXP0000_sample/report|Report]] — `experiment`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|Report]] — `experiment`
- [[lab/05_validation/VAL001/report|Report]] — `validation`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005 — H5 No-Future Walk-Forward Audit]] — `debug_docs`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006 — H5 Live Touch Replay Audit]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
