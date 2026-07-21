---
title: "H0005 — Contextual Branch Regime State"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE.md"
source_ext: ".md"
category: "mql_native_docs"
source_size_bytes: "8248"
entities:
  - "H0002"
  - "H0003"
  - "H0004"
  - "H0005"
  - "M0004"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "NDS Anatomy"
  - "Rally"
  - "Structural Nodes"
  - "Validation"
---


# H0005 — Contextual Branch Regime State

**Source:** [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE.md]]

**Category:** `mql_native_docs`  
**Status:** ok  
**Size:** `8248` bytes

## خلاصه

H0005 is the next research layer after H0004. H0004 proves that reversal/continuation labels are not iid and that branch labels form local event-time regimes. H0005 asks whether the market state is better described by a richer context than the immediately previous branch. A human looking at a chart does not only remember the last touch or the last exit. A human sees that the market has been behaving in a continuation-heavy or reversal-heavy way for a local period. The human eye naturally compresses multiple recent events into a regime impression. H0005 formalizes that intuition with a past-only context vector. For each event `i`, H0005/M0004-v1.03 can compute: The current event's label is ne

## Headings

- H0005 — Contextual Branch Regime State
-   Research question
-   Why this is closer to human perception
-   Past-only context vector
-   Two-mode design
-   Main decision metric
-   Context quality metrics
-   Stress requirements
-   Strategy relevance
-   Consensus state — lastBranch + human-eye context
-   Consensus quality layer — v1.04
-     Core distinction

## Entities

`H0002`, `H0003`, `H0004`, `H0005`, `M0004`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001 — Structural Highs and Lows as Decision Nodes]] — `hypothesis`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007 — H5 Causal Live Replay Audit]] — `debug_docs`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence]] — `mql_native_docs`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity]] — `mql_native_docs`
- [[docs/mql_native/H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE|H0001 — Structural Node Territory Volatility]] — `mql_native_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
