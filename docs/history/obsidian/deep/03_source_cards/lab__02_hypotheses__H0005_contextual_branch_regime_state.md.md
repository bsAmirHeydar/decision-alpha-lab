
---
type: source_card
source_path: "lab/02_hypotheses/H0005_contextual_branch_regime_state.md"
source_ext: ".md"
source_size: 1679
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "UI / React", "Zone / RTV"]
entities: ["H0001", "H0002", "H0003", "H0004", "H0005", "M0001", "M0002", "M0003", "M0004"]
---

# Source Card — H0005_contextual_branch_regime_state.md

## Source

[[lab/02_hypotheses/H0005_contextual_branch_regime_state|lab/02_hypotheses/H0005_contextual_branch_regime_state.md]]

## Summary

Branch behavior is not only a function of the immediately previous reversal/continuation label. A wider past-only context made of recent branch composition, run length, event spacing, pre-volatility, session, trend, and… H0001/M0001: exact structural node events and RTV H0002/M0002: exact reversal/continuation labels H0003/M0003: volatility inertia/memory H0004/M0004: last-event branch-label inertia and run clustering Implemented as the contextual extension of M0004 build 1.02. When last branch and wider context disagree, compare: If wider context wins in disagreement cases and survives engineered nulls, branch-regime is contextual, not merely last-event Markov memory. H0005 now includes a dedicated consensus state: This models the practical human reading of the chart: the last local reaction and the broader recent branch context both point to the same branch. It is reported as: The key

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, H0003, H0004, H0005, M0001, M0002, M0003, M0004

## Headings

- H0005 — Contextual Branch Regime State
  - Hypothesis
  - Base modules
  - Current implementation
  - Core test
  - v1.03 extension — consensus state

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `48`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `48`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `48`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `43`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `38`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `38`
- [[README|README.md]] — score `38`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001_structural_highs_lows_as_decision_nodes.md]] — score `37`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `33`
- [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|H0005_CONTEXTUAL_BRANCH_REGIME_STATE.md]] — score `33`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
