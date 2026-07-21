---
title: "M0001 Consumed Node Repair"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_CONSUMED_NODE_REPAIR.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "849"
entities:
  - "M0001"
concepts:
  - "Convexity"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Consumed Node Repair

**Source:** [[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|docs/mql_native/M0001_CONSUMED_NODE_REPAIR.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `849` bytes

## خلاصه

Once a node is consumed/hunted, its job is finished. For a consumed node: The expansion extreme is a live decision variable only while the node is still active. `DAL_M0001ComputeNodeAuditStates()` now stops scanning a node immediately when it is consumed/hunted. It does not continue updating the expansion extreme after the consume candle. Active nodes can show: Consumed nodes show only an optional marker: The structural node remains on the chart for audit history, but the active extreme and live hunt zone disappear after consumption. Version: `1.22`.

## Headings

- M0001 Consumed Node Repair
-   Rule
-   Engine change
-   Visual change
-   Important

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
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001 Final Visuals and Logic Lock]] — `mql_native_docs`
- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001 Professional Validation Metrics — v1.60]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001 Fast Final-Only Runtime]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
