---
title: "M0001 Exit-Gap Both-Sides Repair"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_EXIT_GAP_BOTH_SIDES_REPAIR.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "1389"
entities:
  - "H0002"
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# M0001 Exit-Gap Both-Sides Repair

**Source:** [[docs/mql_native/M0001_EXIT_GAP_BOTH_SIDES_REPAIR|docs/mql_native/M0001_EXIT_GAP_BOTH_SIDES_REPAIR.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `1389` bytes

## خلاصه

This repair locks the event lifecycle around the completed exit window. A touch event is completed only after `exit_gap` consecutive candles whose high/low do not intersect the frozen event territory. The exit can complete on either side of the frozen zone: rejection/reversal side, break/continuation side. The event must not be discarded simply because the node price was crossed during the pending touch window. The consume input still controls node lifecycle: `DAL_M0001_CONSUME_BY_TOUCH`: a confirmed touch consumes the node at the completed exit candle. `DAL_M0001_CONSUME_BY_HUNT`: a confirmed touch does not consume the node unless the node was hunted/broken during that completed touch event

## Headings

- M0001 Exit-Gap Both-Sides Repair
-   Correct rule
-   Consumption timing
-   RTV
-   H0002 dependency

## Entities

`H0002`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/M0001_H0001_LOGIC_REPAIR_AUDIT|M0001 / H0001 Logic Repair Audit]] — `mql_native_docs`
- [[docs/ui/ROADMAP|UI Implementation Roadmap]] — `ui_docs`
- [[docs/ui/VISUALIZATION_API|Visualization API Contract]] — `ui_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
