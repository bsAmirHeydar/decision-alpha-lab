---
title: "H0001-H0004 Research Lock"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/H0001_H0004_RESEARCH_LOCK.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "8146"
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


# H0001-H0004 Research Lock

**Source:** [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|docs/mql_native/H0001_H0004_RESEARCH_LOCK.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `8146` bytes

## خلاصه

This document audits the first four MQL-native Decision Alpha Lab hypotheses as one layered research stack. It answers two questions: 1. Are the four implemented hypotheses the same hypotheses that were discussed? 2. What still remains open before these facts can be converted into a trading strategy? Current active build targets in this snapshot: M0001 is the base event engine. M0002, M0003, and M0004 must not build independent event universes. They inherit completed M0001 events and M0002 branch labels. A report is part of the locked stack only if it respects these guards: Forbidden old semantics: Structural highs/lows are not arbitrary points. Completed node-territory touch events should h

## Headings

- H0001-H0004 Research Lock
-   Runtime target map
-   Non-negotiable stack guard
-   H0001 — Structural node volatility fact
-     Intended hypothesis
-     Implemented algorithm
-     Status
-   H0002 — Branch volatility model
-     Intended hypothesis
-     Implemented algorithm
-     Branch definition
-     Status

## Entities

`H0001`, `H0002`, `H0003`, `H0004`, `M0001`, `M0002`, `M0003`, `M0004`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002 — Reversal vs Continuation Branch Volatility Model]] — `mql_native_docs`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001 — Structural Highs and Lows as Decision Nodes]] — `hypothesis`
- [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|H0005 — Contextual Branch Regime State]] — `mql_native_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002 Deep Audit and Stability Suite]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
