---
title: "H0002 Deep Audit"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility_deep_audit.md"
source_ext: ".md"
category: "hypothesis"
source_size_bytes: "987"
entities:
  - "H0001"
  - "H0002"
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "NDS Anatomy"
  - "Validation"
---


# H0002 Deep Audit

**Source:** [[lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility_deep_audit|lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility_deep_audit.md]]

**Category:** `hypothesis`  
**Status:** ok  
**Size:** `987` bytes

## خلاصه

H0002 splits completed M0001 exit events into reversal and continuation branches by close versus the original node price at the completed exit candle. It must not filter by hunt/touch outcome before classification. It must not measure a separate post-outcome fixed window by default. The branch label splits the same M0001 event RTV. Primary evidence lines: Full stability lines for each branch: H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.

## Headings

- H0002 Deep Audit
-   Logic repair v1.70

## Entities

`H0001`, `H0002`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility|H0002 — Reversal vs Continuation Node-Exit Volatility Model]] — `hypothesis`
- [[lab/02_hypotheses/H0001_structural_highs_lows_as_decision_nodes|H0001 — Structural Highs and Lows as Decision Nodes]] — `hypothesis`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
