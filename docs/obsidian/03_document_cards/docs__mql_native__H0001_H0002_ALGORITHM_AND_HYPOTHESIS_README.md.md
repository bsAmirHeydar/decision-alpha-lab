---
title: "H0001 / H0002 Algorithm and Hypothesis README"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "11100"
entities:
  - "H0001"
  - "H0002"
  - "H0003"
  - "H0004"
  - "M0001"
  - "M0002"
  - "M0003"
  - "M0004"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# H0001 / H0002 Algorithm and Hypothesis README

**Source:** [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `11100` bytes

## خلاصه

Version: 1.75 This document is the logic lock for the first two Decision Alpha Lab hypotheses. It is written as a research README, not as a strategy guide. The goal is to make every algorithmic assumption explicit enough that future reports can be audited against it. M0002 does not create a separate event stream. It receives the exact completed events produced by M0001 and only labels them by the side of the completed exit candle relative to the original node price. Do rule-based structural highs/lows produce higher event-window volatility than matched random windows? A node is defined by the L-rule. The pivot candle is the visual marker, but logic starts only after the right-side confirmati

## Headings

- H0001 / H0002 Algorithm and Hypothesis README
-   Current research stack
-   H0001 — Structural node relative territory volatility
-     Research question
-     Structural nodes
-     Live territory construction
-     Touch event
-     Exit logic
-     Consumption mode
-     RTV measurement
-     Random null model
-     H0001 acceptance pattern

## Entities

`H0001`, `H0002`, `H0003`, `H0004`, `M0001`, `M0002`, `M0003`, `M0004`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|VAL0012 — H4 Fast Atomic Main Report]] — `validation`
- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[lab/02_hypotheses/H0001_structural_highs_lows_as_decision_nodes|H0001 — Structural Highs and Lows as Decision Nodes]] — `hypothesis`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
