---
title: "M0001 Revisited Zone Colors"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/M0001_REVISITED_ZONE_COLORS.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "456"
entities:
  - "M0001"
concepts:
  - "NDS Anatomy"
  - "Structural Nodes"
---


# M0001 Revisited Zone Colors

**Source:** [[docs/mql_native/M0001_REVISITED_ZONE_COLORS|docs/mql_native/M0001_REVISITED_ZONE_COLORS.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `456` bytes

## خلاصه

When a node survives and receives at least one confirmed revisit, its live zone rectangle changes color: HIGH / peak revisited zone -> purple LOW / valley revisited zone -> blue Rules: Fresh live zones keep the normal node-side colors. Consumed zones still fall back to the consumed/inactive gray history style. Only the rectangle color changes; the revisit logic and state model are unchanged. Version: `1.47`

## Headings

- M0001 Revisited Zone Colors

## Entities

`M0001`

## Concepts

- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001 Candle-Gated Runtime]] — `mql_native_docs`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001 Clean Revisit Labels]] — `mql_native_docs`
- [[docs/mql_native/M0001_CONSUMED_NODE_REPAIR|M0001 Consumed Node Repair]] — `mql_native_docs`
- [[docs/mql_native/M0001_CONSUMED_ZONE_HISTORY|M0001 Consumed Zone History]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001 Excel Audit Report]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXIT_GAP_BOTH_SIDES_REPAIR|M0001 Exit-Gap Both-Sides Repair]] — `mql_native_docs`
- [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|M0001 Extreme and Live Hunt Zone Audit]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
