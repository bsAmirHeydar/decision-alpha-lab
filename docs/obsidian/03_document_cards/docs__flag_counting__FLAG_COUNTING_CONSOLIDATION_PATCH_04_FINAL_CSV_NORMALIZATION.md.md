---
title: "Flag Counting — Consolidation Patch 04 / Final CSV Field Normalization"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2937"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "MQL Native"
  - "Validation"
---


# Flag Counting — Consolidation Patch 04 / Final CSV Field Normalization

**Source:** [[docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION|docs/flag_counting/FLAG_COUNTING_CONSOLIDATION_PATCH_04_FINAL_CSV_NORMALIZATION.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2937` bytes

## خلاصه

This patch is not a new feature level. It does not add Level 31. It does not add execution. It adds a machine-friendly normalized CSV snapshot derived from the final no-send decision state. Consolidation Patch 02 created a human-readable final decision file. Consolidation Patch 04 creates a cleaner version for Excel, Python, dashboards, and automated reports. This is a latest-state snapshot. It is not an append ledger. The normalized CSV uses: Boolean fields are exported as integers: Examples: Direction is exported as both text and sign: Values: The normalized file adds: These are derived from: The normalized file preserves the no-send integrity check. If no-send integrity is broken and the

## Headings

- Flag Counting — Consolidation Patch 04 / Final CSV Field Normalization
-   Purpose
-   New output
-   New inputs
-   What is normalized
-   Boolean columns
-   Direction columns
-   Risk/reward columns
-   No-send integrity
-   Hard boundary
-   Next correct patch

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|EXP0004 — MQL-native M0004 Branch Regime Clustering]] — `experiment`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2|Flag Counting Implementation Checklist V2]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|Flag Counting Level 19 — Phase 14 Entry Geometry Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|Flag Counting Level 19 — Phase 15 Entry Idea Layer]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|Flag Counting Level 19 — Phase 16 Entry Decision Layer / Dry Run]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE17_PAPER_EXECUTION_LEDGER|Flag Counting Level 19 — Phase 17 Paper Execution / Dry Run Ledger]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE22_PAPER_FILTER_DIAGNOSTICS|Flag Counting Level 19 — Phase 22 Paper Filter Diagnostics]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
