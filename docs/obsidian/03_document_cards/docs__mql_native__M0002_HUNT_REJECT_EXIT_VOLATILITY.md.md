---
title: "M0002 Hunt/Reject Document — Deprecated"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0002_HUNT_REJECT_EXIT_VOLATILITY.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "704"
entities:
  - "H0001"
  - "H0002"
  - "M0001"
  - "M0002"
concepts:
  - "NDS Anatomy"
---


# M0002 Hunt/Reject Document — Deprecated

**Source:** [[docs/mql_native/M0002_HUNT_REJECT_EXIT_VOLATILITY|docs/mql_native/M0002_HUNT_REJECT_EXIT_VOLATILITY.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `704` bytes

## خلاصه

This document is kept only as a historical note. The active M0002 module is not hunt/reject based. Use: Current logic: use exact M0001 completed-exit events with hunt/touch consumption preserved, classify the completed-exit candle close relative to `node_price`, and split the original M0001 event-window RTV into `REVERSAL_AFTER_EXIT` and `CONTINUATION_AFTER_EXIT`. H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.

## Headings

- M0002 Hunt/Reject Document — Deprecated
-   Logic repair v1.70

## Entities

`H0001`, `H0002`, `M0001`, `M0002`

## Concepts

- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|M0001 / H0001 Logic Repair Audit]] — `mql_native_docs`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/evidence/h0002_hunt_reject_draft_deprecated/ca2753a3fb76_H0002_hunt_vs_reject_post_exit_volatility|H0002 Hunt/Reject Draft — Deprecated]] — `hypothesis`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
