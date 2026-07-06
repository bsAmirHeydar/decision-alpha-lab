---
title: "M0001 / H0001 Logic Repair Audit"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "2563"
entities:
  - "H0001"
  - "H0002"
  - "M0001"
  - "M0002"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 / H0001 Logic Repair Audit

**Source:** [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `2563` bytes

## خلاصه

Date: 2026-06-18 This document records the logic audit performed before repairing M0002. Structural node territories condition future volatility expansion more than matched random windows. Bars are chronological: oldest to newest. A HIGH node at index `i` requires: `high[i] >= high[i-L..i-1]` `high[i] >= high[i+1..i+L]` A LOW node at index `i` requires: `low[i] <= low[i-L..i-1]` `low[i] <= low[i+1..i+L]` Node becomes knowable at: For LOW nodes, the tracking extreme is the highest high after the active-from point. For HIGH nodes, it is the lowest low after the active-from point. Event starts when a candle intersects the live territory. The event territory freezes at event entry. Exit confirma

## Headings

- M0001 / H0001 Logic Repair Audit
-   H0001 active hypothesis
-   Locked structural-node logic
-   Locked territory logic
-   Locked M0001 event/RTV logic
-   Locked anti-lookahead rules
-   Result of audit

## Entities

`H0001`, `H0002`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
