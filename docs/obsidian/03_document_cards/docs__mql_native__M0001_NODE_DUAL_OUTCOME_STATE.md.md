---
title: "M0001 Node Dual Outcome State"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_NODE_DUAL_OUTCOME_STATE.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1421"
entities:
  - "M0001"
concepts:
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Node Dual Outcome State

**Source:** [[docs/mql_native/M0001_NODE_DUAL_OUTCOME_STATE|docs/mql_native/M0001_NODE_DUAL_OUTCOME_STATE.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1421` bytes

## خلاصه

Version: active semantics preserved in 1.59 Every node stores TOUCH and HUNT information independently of the selected consumption model. The consumption model decides when a node becomes inactive. A zone touch starts only a pending touch event: The touch is confirmed only after strict exit-gap closure: If the node price breaks before touch confirmation: That outcome becomes HUNT. In TOUCH mode: In HUNT mode: Once a node is consumed, no further candles are scanned for that node. The old validation-journal CSV writer is retired. Current audit state is used for final chart drawings and final compact node-vs-random logRTV reports.

## Headings

- M0001 Node Dual Outcome State
-   Purpose
-   Stored on each audit state
-   Logic
-   Consumption model
-   Reporting

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|EXP0002 — MQL-native M0001 Runtime]] — `experiment`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|VAL_M0001_MQL_NATIVE]] — `validation`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|M0001 Consumed Node Repair]] — `mql_native_docs`
- [[docs/mql_native/M0001_CONSUMED_ZONE_HISTORY|M0001 Consumed Zone History]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
