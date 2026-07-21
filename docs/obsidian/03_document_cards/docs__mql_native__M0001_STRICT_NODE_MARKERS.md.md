---
title: "M0001 Strict Node Markers"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_STRICT_NODE_MARKERS.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1003"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "NDS Anatomy"
---


# M0001 Strict Node Markers

**Source:** [[docs/mql_native/M0001_STRICT_NODE_MARKERS|docs/mql_native/M0001_STRICT_NODE_MARKERS.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1003` bytes

## خلاصه

M0001 node visualization is now strict arrow-only. The visual layer no longer draws chevron wing segments for nodes and no longer draws full-chart horizontal node price lines. The only node objects are: Chevron markers are implemented as `OBJ_TREND` segments. On dense M1 charts they look like high/low tracing lines around candles. This is visually noisy and makes node inspection harder. When `InpShowNodePrices=true`: HIGH node price is written above the red down arrow LOW node price is written below the green up arrow Arrow marker anchor typing now uses `ENUM_ARROW_ANCHOR`, not `ENUM_ANCHOR_POINT`, so MetaEditor should no longer warn about implicit enum conversion.

## Headings

- M0001 Strict Node Markers
-   Change
-   Why
-   Inputs
-   Price labels
-   Warning fix

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_ARROW_MARKERS|M0001 Clean Arrow Markers]] — `mql_native_docs`
- [[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|M0001 Fast Final-Only Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001 Final Visuals and Logic Lock]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
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
