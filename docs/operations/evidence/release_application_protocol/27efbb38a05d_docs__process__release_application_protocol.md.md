---
title: "Release Application Protocol"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/operations/evidence/release_application_protocol/9f8ab22f3dfb_release_application_protocol.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "1770"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
---


# Release Application Protocol

**Source:** [[docs/operations/evidence/release_application_protocol/9f8ab22f3dfb_release_application_protocol|docs/operations/evidence/release_application_protocol/9f8ab22f3dfb_release_application_protocol.md]]

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

- [[docs/history/obsidian/base/04_concepts/Execution|Execution]]
- [[docs/history/obsidian/base/04_concepts/MQL_Native|MQL Native]]
- [[docs/operations/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/operations/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/operations/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/operations/process/metatrader_compile_checklist|MetaTrader Compile Checklist]] — `core_docs`
- [[docs/operations/evidence/exp0000_sample/58c8a635ff91_report|Report]] — `experiment`
- [[docs/operations/evidence/exp0001_structural_highs_lows_importance/337872464ffa_report|Report]] — `experiment`
- [[docs/operations/evidence/val001/360462a17ab1_report|Report]] — `validation`
- [[docs/operations/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/history/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005 — H5 No-Future Walk-Forward Audit]] — `debug_docs`
- [[docs/history/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006 — H5 Live Touch Replay Audit]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
