---
title: "M0001 Professional Validation Metrics — v1.60"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "4159"
entities:
  - "M0001"
concepts:
  - "Convexity"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Professional Validation Metrics — v1.60

**Source:** [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `4159` bytes

## خلاصه

This document locks the professional validation layer added to the M0001 MQL-native research engine. The node, territory, touch, HUNT, revisit, RTV, logRTV, warmup, and candle-gated runtime semantics are unchanged. The EA remains candle-gated during runtime: The professional statistics are intentionally final-only. They are not recalculated on every candle. Earlier reports embedded `histRaw` into the main NODES/RANDOM lines. Long histograms could be truncated by the MetaTrader Journal, hiding the important `COMPARE` section. v1.60 fixes this by default: The main final lines are compact and the histogram is printed only as separate optional `DAL_M0001_FINAL_HIST_*` lines. Each node event can

## Headings

- M0001 Professional Validation Metrics — v1.60
-   Final-only validation design
-   Compact report bug fix
-   Random baseline K
-   Core outputs
-     NODES / RANDOM
-     COMPARE
-     QUANT_TAIL
-     ROBUST
-     SESSION_REGIME
-     AUDIT
-   Optional parameter robustness grid

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|M0001 Consumed Node Repair]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001 Final Visuals and Logic Lock]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
