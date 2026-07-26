---
title: "System Architecture"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/architecture.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "3634"
entities:
  - "M0001"
  - "M0002"
  - "M0004"
  - "M0005"
concepts:
  - "AI Agent Layer"
  - "Astro ML"
  - "Atomic No-Sample"
  - "Execution"
  - "Known-Time Causality"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# System Architecture

**Source:** [[docs/architecture|docs/architecture.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `3634` bytes

## خلاصه

Decision Alpha Lab uses a layered architecture for structural market research and execution. The project does not assume that fixed time windows are the natural unit of market analysis. The core unit is a structural event: node, zone, revisit, hunt, break, known-time regime, and execution opportunity. Python remains useful for: data engineering, large-scale offline analysis, feature extraction, visualization, exploratory statistics, parameter sweeps, external data pipelines. Python is allowed to discover ideas. It must not be the only source of live-valid execution claims unless its replay is strictly causal. MQL5 is responsible for: MetaTrader-native replay, Expert Advisor execution, broker

## Headings

- System Architecture
-   Research philosophy
-   Python layer
-   MQL5 layer
-   Core modules
-     M0001 — Structural node and event lifecycle
-     M0002 — Branch sample pairing
-     M0004 — Regime memory
-     M0005 — Directional memory
-   Validation hierarchy
-   Design principle
-   Astro stack

## Entities

`M0001`, `M0002`, `M0004`, `M0005`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/debug/MAIN_ATOMIC_NO_SAMPLE_UNIFICATION|Main Atomic No-Sample Unification for H4/H5]] — `debug_docs`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/evidence/h0004_branch_regime_clustering/9b519b63fc23_H0004_branch_regime_clustering|H0004 — Branch Regime Clustering]] — `hypothesis`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
