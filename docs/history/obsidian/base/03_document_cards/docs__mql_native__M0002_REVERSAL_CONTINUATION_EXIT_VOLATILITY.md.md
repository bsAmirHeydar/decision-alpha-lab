---
title: "M0002 — Reversal vs Continuation After Exit Volatility"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "9348"
entities:
  - "H0001"
  - "H0002"
  - "M0001"
  - "M0002"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0002 — Reversal vs Continuation After Exit Volatility

**Source:** [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `9348` bytes

## خلاصه

Version: 1.66 M0002 tests the second hypothesis in a separate MQL-native module. It reuses M0001 structural-node extraction, territory geometry, log-range math, random-baseline logic, and validation/reporting utilities. It uses the exact M0001 completed-event lifecycle; no separate neutral event stream is built. `M0002_HuntRejectExitVolatility.mq5` remains only as a deprecated compatibility filename and now runs the same reversal/continuation logic. After a structural-node territory touch has completed its strict `exit_gap` window outside the frozen event zone, the completed event is classified only by the completed-exit candle side relative to the original node price. The question is whethe

## Headings

- M0002 — Reversal vs Continuation After Exit Volatility
-   Central Expert Advisor
-   Include stack
-   Core hypothesis
-   Event construction
-   Branch rules
-   Primary measurement window
-   Optional diagnostic mode
-   Inputs
-   Reports
-   v1.67 EVENT_RTV lock
-   Deep audit repair notes

## Entities

`H0001`, `H0002`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|M0001 / H0001 Logic Repair Audit]] — `mql_native_docs`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
