---
title: "Main Atomic No-Sample Unification for H4/H5"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "1911"
entities:
  - "M0001"
  - "M0002"
  - "M0004"
  - "M0005"
concepts:
  - "Atomic No-Sample"
  - "Execution"
  - "Known-Time Causality"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Main Atomic No-Sample Unification for H4/H5

**Source:** [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `1911` bytes

## خلاصه

This release moves the no-sample / live-style contract into the main M0004 and M0005 experts. The main reports now default to atomic raw M0001 event replay: no `DALM0002BranchSample` sequence is built by the official main report path no M0002 branch-sample collector is called by the official main report path regime order is based on the candle/time at which raw M0001 events become knowable raw events known on the same candle are treated as simultaneous mixed reversal/continuation batches are marked ambiguous and skipped from transition/path statistics by default `M0004_BranchRegimeClustering.mq5` now calls `DAL_M0004RunAtomicNoSampleReport()` by default. Official audit line: The legacy sampl

## Headings

- Main Atomic No-Sample Unification for H4/H5
-   Contract
-   M0004
-   M0005
-   Why

## Entities

`M0001`, `M0002`, `M0004`, `M0005`

## Concepts

- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|H4 Deep Atomic Report + H6 Reversal Optionality]] — `debug_docs`
- [[docs/debug/H6_NODE_SURVIVAL_MAP|H6 Node Survival Map]] — `debug_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/process/metatrader_compile_checklist|MetaTrader Compile Checklist]] — `core_docs`
- [[docs/evidence/h0004_branch_regime_clustering/9b519b63fc23_H0004_branch_regime_clustering|H0004 — Branch Regime Clustering]] — `hypothesis`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
