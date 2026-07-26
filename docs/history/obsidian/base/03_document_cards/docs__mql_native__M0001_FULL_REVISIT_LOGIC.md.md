---
title: "M0001 Full Revisit Logic"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_FULL_REVISIT_LOGIC.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1862"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# M0001 Full Revisit Logic

**Source:** [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|docs/mql_native/M0001_FULL_REVISIT_LOGIC.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1862` bytes

## خلاصه

A revisit is a completed territory interaction event for a node that has not yet been consumed. A revisit starts when a candle intersects the current live territory zone: At this exact entry candle, event geometry freezes: While the event is active: This prevents the current revisit from repainting, while still keeping the node's future territory correct if the node remains alive. A pending touch becomes confirmed only after: using the frozen event zone. HUNT always has priority before touch confirmation: If this happens during a pending revisit, that revisit closes as HUNT and the node is consumed by HUNT. TOUCH mode: HUNT mode: New visual inputs: Labels: `M0001_LiveVisualLab.mq5` version:

## Headings

- M0001 Full Revisit Logic
-   Revisit definition
-   Start condition
-   Active event
-   Touch confirmation
-   HUNT priority
-   Consumption modes
-   Visuals
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_RTV_LOG_HILO|M0001 RTV — Log High/Low Volatility]] — `mql_native_docs`
- [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|M0001 Viewport Visual Renderer]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001 Clean Revisit Labels]] — `mql_native_docs`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXIT_GAP_BOTH_SIDES_REPAIR|M0001 Exit-Gap Both-Sides Repair]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
