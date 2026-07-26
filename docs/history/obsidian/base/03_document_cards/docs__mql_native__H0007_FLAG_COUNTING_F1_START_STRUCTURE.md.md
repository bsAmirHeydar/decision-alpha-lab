---
title: "H0007 — Flag Counting / F1 Start Structure"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "31681"
entities:
  - "H0001"
  - "H0002"
  - "H0004"
  - "H0005"
  - "H0006"
  - "H0007"
  - "M0001"
  - "M0007"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "Known-Time Causality"
  - "MQL Native"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# H0007 — Flag Counting / F1 Start Structure

**Source:** [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `31681` bytes

## خلاصه

> Status: design lock, topology-only. > Version: v0.2 — nested `R12` rule added and expanded. > Layer: structural grammar on top of the M0001 final-only known-time node stream. > Scope: define and audit **F1 only**. F2 and F3 are intentionally out of scope until F1 is mechanically stable. The purpose of this README is to turn the visual idea of **F1** into a mechanical object. F1 must not remain a drawing. It must become something that the code can count, draw, invalidate, confirm, export, and later compare against random baselines. This document is therefore not a trading strategy. It is a **structural counting contract**. The detector must answer one narrow question first: Only after that

## Headings

- H0007 — Flag Counting / F1 Start Structure
-   0. Why this document exists
-   1. Core thesis
-   2. Reference sketches
-   3. Critical corrections locked in v0.2
-     3.1 `R12` break is not final confirmation
-     3.2 `R12` must stay inside the main second extreme
-   4. Canonical naming
-     4.1 Bullish F1 names
-     4.2 Bearish F1 names
-   5. F1 is not a trade
-   6. Source contract: known-time nodes only

## Entities

`H0001`, `H0002`, `H0004`, `H0005`, `H0006`, `H0007`, `M0001`, `M0007`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/evidence/h0007_flag_counting_f1_start_structure/d02c831e47bd_H0007_flag_counting_f1_start_structure|H0007 — Flag Counting / F1 Start Structure]] — `hypothesis`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001 — Structural Highs and Lows as Decision Nodes]] — `hypothesis`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002 — Reversal vs Continuation After Exit Volatility]] — `mql_native_docs`
- [[lab/05_validation/VAL0011_main_atomic_no_sample_unification/README|VAL0011 — Main Atomic No-Sample Unification]] — `validation`
- [[lab/09_execution/mql5/README|MQL5 Execution and Validation Layer]] — `execution`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|EXP0003 — M0002 Reversal/Continuation Exit Volatility]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
