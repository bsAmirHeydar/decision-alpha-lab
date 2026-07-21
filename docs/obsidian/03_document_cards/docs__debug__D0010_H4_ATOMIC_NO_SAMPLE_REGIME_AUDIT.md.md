---
title: "D0010 — H4 Atomic No-Sample Regime Audit"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "1554"
entities:
  - "D0010"
  - "H0004"
  - "M0001"
  - "M0002"
  - "M0004"
concepts:
  - "AI Agent Layer"
  - "Atomic No-Sample"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# D0010 — H4 Atomic No-Sample Regime Audit

**Source:** [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `1554` bytes

## خلاصه

D0010 is the strict live-style validator for H0004 regime memory. It removes M0002 branch samples from the H4 validation path: no `DALM0002BranchSample` no `DAL_M0002CollectBranchSamples` no outcome-sorted sample sequence no artificial sequencing of regimes that become knowable on the same candle At each replay step, D0010 uses only closed bars available up to that candle: 1. Build confirmed structural nodes from the prefix. 2. Build raw M0001 events from the prefix. 3. Classify only raw events whose `known_index` equals the current decision candle. 4. Treat all events with the same `known_time` as one simultaneous batch. 5. If a batch contains both reversal and continuation labels, mark it

## Headings

- D0010 — H4 Atomic No-Sample Regime Audit
-   Contract
-   Important output lines
-   Interpretation

## Entities

`D0010`, `H0004`, `M0001`, `M0002`, `M0004`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Atomic_No-Sample|Atomic No-Sample]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/05_validation/VAL0010_h4_atomic_no_sample_regime/README|VAL0010 — H4 Atomic No-Sample Regime Validation]] — `validation`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/evidence/h0004_branch_regime_clustering/9b519b63fc23_H0004_branch_regime_clustering|H0004 — Branch Regime Clustering]] — `hypothesis`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4 Fast Atomic Main Report]] — `debug_docs`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[lab/03_validation/VAL0012_h4_fast_atomic_main/README|VAL0012 — H4 Fast Atomic Main Report]] — `validation`
- [[README|Decision Alpha Lab]] — `readme`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
