---
title: "MetaTrader Compile Checklist"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/process/metatrader_compile_checklist.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "1470"
entities:
  - "M0001"
  - "M0004"
  - "M0005"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
---


# MetaTrader Compile Checklist

**Source:** [[docs/process/metatrader_compile_checklist|docs/process/metatrader_compile_checklist.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `1470` bytes

## خلاصه

Use this checklist after applying any MQL5 release. Close MetaEditor before applying the release. Apply ZIP or PATCH, not both. Run the release installer if one exists. Reopen MetaEditor. Compile shared include changes through the Experts that use them. Suggested order: 1. M0001 / node and event Experts, 2. M0004 / regime memory Experts, 3. M0005 / directional memory Experts, 4. Debug validators, 5. Execution EAs. If compile fails, capture the full MetaEditor error list. Do not summarize from memory. A useful error report contains: file path, line number, column number, exact error text, whether the file is repo-level or terminal include-level. The repo include changed, but MetaEditor is rea

## Headings

- MetaTrader Compile Checklist
-   Before compile
-   Compile order
-   Error handling
-   Frequent failure modes
-     Include mismatch
-     Enum mismatch
-     Function signature mismatch
-     Debug-only logic not promoted

## Entities

`M0001`, `M0004`, `M0005`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|Main Atomic No-Sample Unification for H4/H5]] — `debug_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/evidence/h0004_branch_regime_clustering/9b519b63fc23_H0004_branch_regime_clustering|H0004 — Branch Regime Clustering]] — `hypothesis`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
