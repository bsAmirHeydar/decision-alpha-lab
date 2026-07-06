
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY.md"
source_ext: ".md"
source_size: 3951
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Path Smoothness", "Python Brain", "Rally", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY.md

## Source

[[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY|docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE27_PAPER_MFE_MAE_PATH_QUALITY.md]]

## Summary

Phase 27 adds paper MFE / MAE path quality diagnostics above the Phase 26 Paper Performance Report. This phase still does **not** send real orders. It evaluates persistent paper trade lifecycle rows and produces close-only path quality metrics: Phase 27 writes: The State Gate snapshot now stores: Each row exports: Phase 27 is still close-only. It does **not** yet use intrabar high/low over the full path. So the values are deliberately named: The goal is not fake precision. The goal is to begin measuring path quality in a conservative, audit-friendly way. Examples: Examples: This phase supports the project objective of measuring path cleanliness, not only final outcome. It starts answering: Every Phase 27 row keeps: No order is opened, modified, deleted, closed, or sent. Phase 27 does not modify: It only reads persistent paper trade lifecycle rows and writes paper path quality diagnostics

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Level 19 — Phase 27 Paper MFE / MAE Path Quality
  - Purpose
  - Hard safety contract
  - New CSV
  - New input
  - Snapshot-level fields
  - Row-level metrics
  - Important limitation
  - Buckets
  - Pullback pressure statuses
  - Why this matters
  - Execution safety

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX|FLAG_COUNTING_LEVEL_19_PHASE28_CONTEXT_PERFORMANCE_MATRIX.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS|FLAG_COUNTING_LEVEL_19_PHASE14_ENTRY_GEOMETRY_READINESS.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER|FLAG_COUNTING_LEVEL_19_PHASE15_ENTRY_IDEA_LAYER.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN|FLAG_COUNTING_LEVEL_19_PHASE16_ENTRY_DECISION_DRY_RUN.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE20_PAPER_PORTFOLIO_AGGREGATE_METRICS|FLAG_COUNTING_LEVEL_19_PHASE20_PAPER_PORTFOLIO_AGGREGATE_METRICS.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
