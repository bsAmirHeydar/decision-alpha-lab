---
title: "M0001 Stress Validation Suite"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_STRESS_VALIDATION_SUITE.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "4826"
entities:
  - "M0001"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Stress Validation Suite

**Source:** [[docs/mql_native/M0001_STRESS_VALIDATION_SUITE|docs/mql_native/M0001_STRESS_VALIDATION_SUITE.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `4826` bytes

## خلاصه

Version: 1.61 This document locks the additional validation layer around M0001. The structural-node, territory, touch/HUNT, revisit, RTV, logRTV, warmup, analysis-start, and final visual semantics are unchanged. Version 1.61 adds final-only stress reports that try to break the node-vs-random volatility-expansion fact under harder nulls. The EA remains candle-gated and final-only by default: No stress test changes the event definition. Stress tests operate after the final event set is built. `InpBrokerUtcOffsetHours` converts broker-server hour to UTC hour for session reports. If broker time is UTC+2, set it to `2`. If broker time is UTC+3, set it to `3`. `InpRegimeLookbackBars` defines the p

## Headings

- M0001 Stress Validation Suite
-   Runtime principle
-   New inputs
-   Final stress reports
-     HARD_NULL
-     PLACEBO
-     OUTLIER_STRESS
-     NONOVERLAP
-     CLUSTER_ROBUST
-     BLOCK_BOOT
-     HORIZON
-     NEGATIVE_CONTROL

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|M0001 Consumed Node Repair]] — `mql_native_docs`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001 Final Visuals and Logic Lock]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
