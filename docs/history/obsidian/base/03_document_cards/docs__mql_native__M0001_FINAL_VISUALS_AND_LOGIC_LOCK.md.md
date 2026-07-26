---
title: "M0001 Final Visuals and Logic Lock"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "6535"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Final Visuals and Logic Lock

**Source:** [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `6535` bytes

## خلاصه

Version: 1.59 This document locks the current M0001 research semantics and runtime contract. It exists so future optimization work does not accidentally change the algorithm. M0001 is candle-based, not tick-based. The optimized default is: That means: no full node/event recomputation on every closed candle, no chart object deletion/redraw loop during the test, final node/random logRTV reports are printed once at shutdown, final chart objects are restored and kept after the run finishes. For visual debugging during a replay, set: This intentionally costs more because the chart state is recomputed and redrawn on each newly closed candle. A confirmed L-rule node at index `i` requires both left

## Headings

- M0001 Final Visuals and Logic Lock
-   Runtime contract
-   Structural node definition
-   Territory formula
-   Event lifecycle
-   HUNT priority
-   TOUCH mode
-   HUNT mode and revisit memory
-   Revisited-live extreme reset
-   Visual rules
-   RTV and logRTV
-   Warmup and analysis period

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001 Professional Validation Metrics — v1.60]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|M0001 Consumed Node Repair]] — `mql_native_docs`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001 Fast Final-Only Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
