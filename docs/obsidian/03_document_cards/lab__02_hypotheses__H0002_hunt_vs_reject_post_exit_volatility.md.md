---
title: "H0002 Hunt/Reject Draft — Deprecated"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/h0002_hunt_reject_draft_deprecated/ca2753a3fb76_H0002_hunt_vs_reject_post_exit_volatility.md"
source_ext: ".md"
category: "hypothesis"
source_size_bytes: "843"
entities:
  - "H0001"
  - "H0002"
  - "M0001"
  - "M0002"
concepts:
  - "MQL Native"
  - "NDS Anatomy"
---


# H0002 Hunt/Reject Draft — Deprecated

**Source:** [[docs/evidence/h0002_hunt_reject_draft_deprecated/ca2753a3fb76_H0002_hunt_vs_reject_post_exit_volatility|docs/evidence/h0002_hunt_reject_draft_deprecated/ca2753a3fb76_H0002_hunt_vs_reject_post_exit_volatility.md]]

**Category:** `hypothesis`  
**Status:** ok  
**Size:** `843` bytes

## خلاصه

This draft is kept only for history. It is not the active H0002 definition. The active hypothesis is: The active implementation is: Reason for deprecation: the second hypothesis is not a hunt/non-hunt split. It is a M0001 completed-exit branch split by the completed-exit candle close relative to the original node price, with the primary metric equal to the same M0001 event-window RTV split by branch. H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.

## Headings

- H0002 Hunt/Reject Draft — Deprecated
-   Logic repair v1.70

## Entities

`H0001`, `H0002`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility|H0002 — Reversal vs Continuation Node-Exit Volatility Model]] — `hypothesis`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
