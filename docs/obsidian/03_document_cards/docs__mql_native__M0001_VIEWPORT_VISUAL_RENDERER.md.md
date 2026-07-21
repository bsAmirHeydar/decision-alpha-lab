---
title: "M0001 Viewport Visual Renderer"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1219"
entities:
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# M0001 Viewport Visual Renderer

**Source:** [[docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER|docs/mql_native/M0001_VIEWPORT_VISUAL_RENDERER.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1219` bytes

## خلاصه

The M0001 engine can compute hundreds of nodes and audit states. Drawing every node, every price label, every consumed marker, every extreme line, and every hunt-zone rectangle on one MT5 chart can overload chart-object rendering. This can look like nodes stop appearing after a point even though the detector is still computing them. The renderer now defaults to viewport-based drawing: The engine still computes all data. The chart only draws objects whose time range intersects the currently visible chart window plus padding. When the chart is scrolled or zoomed, `OnChartEvent(CHARTEVENT_CHART_CHANGE)` redraws the objects for the new viewport. This is not a research/data limit. still means all

## Headings

- M0001 Viewport Visual Renderer
-   Problem
-   Fix
-   Important distinction
-   Summary
-   Version

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|M0001 Final-Only Research Report, Warmup, and MQL Prune]] — `mql_native_docs`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001 Final Visuals and Logic Lock]] — `mql_native_docs`
- [[docs/mql_native/M0001_FULL_REVISIT_LOGIC|M0001 Full Revisit Logic]] — `mql_native_docs`
- [[docs/evidence/m0001_json_audit/2e8468dd6e0a_M0001_JSON_AUDIT_REPORT|M0001 JSON Audit Report]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
