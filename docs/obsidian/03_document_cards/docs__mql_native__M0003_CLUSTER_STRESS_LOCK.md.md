---
title: "M0003 Cluster Stress Lock"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0003_CLUSTER_STRESS_LOCK.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1074"
entities:
  - "H0001"
  - "H0002"
  - "H0003"
  - "M0002"
  - "M0003"
concepts:
  - "AI Agent Layer"
  - "Validation"
---


# M0003 Cluster Stress Lock

**Source:** [[docs/mql_native/M0003_CLUSTER_STRESS_LOCK|docs/mql_native/M0003_CLUSTER_STRESS_LOCK.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1074` bytes

## خلاصه

This update hardens H0003 from a simple continuation-memory diagnostic into a full cluster-stress suite. Split M0003 inertia output into short non-truncated reports. Added per-horizon memory reports for each configured horizon. Added memory AUC and carry AUC summary. Added direct cluster comparison between reversal and continuation. Added deterministic Fisher-Yates lag-shuffle stress for lag-1 and lag-2 serial memory, with empirical p-values. Added direct branch-label permutation stress to test whether continuation-specific cluster memory survives label randomization. Added contiguous block cluster stress. Added configurable high-volatility run percentile. Added high-run iid expectation and

## Headings

- M0003 Cluster Stress Lock
-   Changes
-   Build targets

## Entities

`H0001`, `H0002`, `H0003`, `M0002`, `M0003`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE|H0001 — Structural Node Territory Volatility]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
