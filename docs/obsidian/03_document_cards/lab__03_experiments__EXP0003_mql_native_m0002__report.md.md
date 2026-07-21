---
title: "EXP0003 — M0002 Reversal/Continuation Exit Volatility"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0003_mql_native_m0002/report.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "956"
entities:
  - "EXP0003"
  - "H0001"
  - "H0002"
  - "M0001"
  - "M0002"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# EXP0003 — M0002 Reversal/Continuation Exit Volatility

**Source:** [[lab/03_experiments/EXP0003_mql_native_m0002/report|lab/03_experiments/EXP0003_mql_native_m0002/report.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `956` bytes

## خلاصه

This experiment runs the M0002 central Expert Advisor. It reuses M0001 structural-node detection, territory math, log-range utilities, and reporting metrics, but uses M0001 completed-exit events with M0001 hunt/touch consumption filtering preserved. It then separates completed post-exit events into `REVERSAL_AFTER_EXIT` and `CONTINUATION_AFTER_EXIT` branches based on the node-side of the exit-completion candle. Expected output prefixes: H0002 now uses `DAL_M0001ComputeEvents()` directly. Node lifetime is preserved exactly as in H0001/M0001. The selected `InpConsumeMode` decides whether a confirmed touch consumes the node or whether the node remains alive and recomputes the next cycle until a

## Headings

- EXP0003 — M0002 Reversal/Continuation Exit Volatility
-   Logic repair v1.70

## Entities

`EXP0003`, `H0001`, `H0002`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|M0001 / H0001 Logic Repair Audit]] — `mql_native_docs`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`
- [[docs/evidence/h0002_hunt_reject_draft_deprecated/ca2753a3fb76_H0002_hunt_vs_reject_post_exit_volatility|H0002 Hunt/Reject Draft — Deprecated]] — `hypothesis`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
