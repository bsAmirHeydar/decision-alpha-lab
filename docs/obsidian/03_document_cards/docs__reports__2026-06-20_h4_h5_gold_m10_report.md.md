---
title: "Report — H4/H5 GOLD M10 Review, 2026-06-20"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/reports/2026-06-20_h4_h5_gold_m10_report.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "3323"
entities:
  - "H0004"
  - "H0005"
  - "M0001"
  - "M0002"
concepts:
  - "AI Agent Layer"
  - "Atomic No-Sample"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# Report — H4/H5 GOLD M10 Review, 2026-06-20

**Source:** [[docs/reports/2026-06-20_h4_h5_gold_m10_report|docs/reports/2026-06-20_h4_h5_gold_m10_report.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `3323` bytes

## خلاصه

This report summarizes the project findings from the GOLD M10 H4/H5 logs and the subsequent code-audit discussion. Instrument: GOLD Timeframe: M10 Bars: approximately 21,370 M0001 events: approximately 3,197 Classic M0002 paired branch labels: approximately 2,484 The classic H4 sample sequence reported strong regime inertia: same-label transition rate: 72.82%, same lift over IID: 19.80 percentage points, lag-1 correlation: 0.4214. After causal known-candle batching: pure known-time batches: 1,807, ambiguous mixed-energy batches: 40, same-candle batch count: 441, causal same-label transition rate: 65.61%, causal same lift: 11.98 percentage points, causal lag-1 correlation: 0.2584. Interpretat

## Headings

- Report — H4/H5 GOLD M10 Review, 2026-06-20
-   Dataset context
-   H0004 classic vs causal-batch result
-   H0005 classic path result
-     Reversal
-     Continuation
-   Official conclusion
-   Decision impact
-     Reversal execution
-     Continuation execution

## Entities

`H0004`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/articles/structural_regime_memory_without_samples|Article — Structural Regime Memory Without Samples]] — `article_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
