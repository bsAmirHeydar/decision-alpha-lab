---
title: "H0004 — Branch Regime Memory"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic.md"
source_ext: ".md"
category: "hypothesis"
source_size_bytes: "2301"
entities:
  - "H0004"
  - "H0005"
  - "M0001"
  - "M0002"
concepts:
  - "AI Agent Layer"
  - "Atomic No-Sample"
  - "Convexity"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# H0004 — Branch Regime Memory

**Source:** [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic.md]]

**Category:** `hypothesis`  
**Status:** ok  
**Size:** `2301` bytes

## خلاصه

id: H0004 status: active_rebuilt family: regime_memory official_contract: atomic_no_sample_known_time_batches created: 2026-06-20 owner: Decision Alpha Lab priority: critical Do reversal and continuation branch regimes display persistence beyond random ordering when measured by the time at which the regime became knowable? The classic formulation used M0002 branch samples and sorted completed labels into a chronological sequence. This was useful for exploration, but it had a serious live-validity risk: several labels could become known on the same candle and still be ordered as if one came before another. The official H0004 formulation is atomic and no-sample: 1. replay closed candles, 2. bu

## Headings

- H0004 — Branch Regime Memory
-   Research question
-   Old formulation
-   Current formulation
-   Null hypothesis
-   Alternative hypothesis
-   Key failure mode addressed
-   Evidence required
-   Interpretation

## Entities

`H0004`, `H0005`, `M0001`, `M0002`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/evidence/h0004_branch_regime_clustering/9b519b63fc23_H0004_branch_regime_clustering|H0004 — Branch Regime Clustering]] — `hypothesis`
- [[docs/evidence/h0005_directional_memory_execution/57d9666c6533_H0005_directional_memory_atomic|H0005 — Directional Memory and Execution]] — `hypothesis`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001 — Structural Highs and Lows as Decision Nodes]] — `hypothesis`
- [[docs/articles/structural_regime_memory_without_samples|Article — Structural Regime Memory Without Samples]] — `article_docs`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
