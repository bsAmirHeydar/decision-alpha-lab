---
title: "MQL-Native Runtime Architecture"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/MQL_NATIVE_ARCHITECTURE.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1909"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# MQL-Native Runtime Architecture

**Source:** [[docs/mql_native/MQL_NATIVE_ARCHITECTURE|docs/mql_native/MQL_NATIVE_ARCHITECTURE.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1909` bytes

## خلاصه

Version: 1.59 The active runtime is MQL5-native. Python, FastAPI, React, Parquet caches, CSV bridges, Excel/JSON report generation, and external watcher loops are not part of the active execution path. Fast final-only mode: Visual replay mode: MQL5 is the source of truth for: candle access, warmup historical seeding, L-rule structural node detection, M0001 territory/event construction, HUNT/TOUCH/revisit semantics, RTV/logRTV calculation, matched random baseline, final chart visualization. The canonical active semantics are documented in:

## Headings

- MQL-Native Runtime Architecture
-   Decision
-   Active runtime flow
-   Source of truth
-   Active module layout
-   Removed from active runtime
-   Logic lock

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001 Final Visuals and Logic Lock]] — `mql_native_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/evidence/m0001_json_audit/2e8468dd6e0a_M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
