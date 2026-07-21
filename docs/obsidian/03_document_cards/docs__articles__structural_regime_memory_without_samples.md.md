---
title: "Article — Structural Regime Memory Without Samples"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/articles/structural_regime_memory_without_samples.md"
source_ext: ".md"
category: "article_docs"
source_size_bytes: "2823"
entities:
  - "H0004"
  - "M0001"
  - "M0002"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Validation"
---


# Article — Structural Regime Memory Without Samples

**Source:** [[docs/articles/structural_regime_memory_without_samples|docs/articles/structural_regime_memory_without_samples.md]]

**Category:** `article_docs`  
**Status:** ok  
**Size:** `2823` bytes

## خلاصه

A central question of Decision Alpha Lab is whether structural market regimes have memory. Early reports suggested that reversal and continuation labels cluster: a reversal label is more likely to be followed by another reversal, and a continuation label is more likely to be followed by another continuation. A key flaw was then identified: several labels may become knowable on the same candle. If those labels are sorted into a sequence, the report can create transitions that never existed in live time. This article documents the move from sample sequencing to atomic known-time regime batching. Branch samples are convenient. They compress a market event into one object with entry, exit, outco

## Headings

- Article — Structural Regime Memory Without Samples
-   Abstract
-   The problem with sample order
-   The same-candle sequencing flaw
-   Atomic known-time batches
-   Why this matters
-   The current standard

## Entities

`H0004`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/evidence/h0004_branch_regime_clustering/9b519b63fc23_H0004_branch_regime_clustering|H0004 — Branch Regime Clustering]] — `hypothesis`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[docs/debug/H4_ATOMIC_FULL_STRESS_CONTEXT|H4 Atomic Full Stress + Human Context Diagnostics]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
