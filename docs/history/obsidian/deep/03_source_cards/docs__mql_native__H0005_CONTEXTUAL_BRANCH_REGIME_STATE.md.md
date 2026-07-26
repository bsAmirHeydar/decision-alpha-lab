
---
type: source_card
source_path: "docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE.md"
source_ext: ".md"
source_size: 8248
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0002", "H0003", "H0004", "H0005", "M0004"]
---

# Source Card — H0005_CONTEXTUAL_BRANCH_REGIME_STATE.md

## Source

[[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE.md]]

## Summary

H0005 is the next research layer after H0004. H0004 proves that reversal/continuation labels are not iid and that branch labels form local event-time regimes. H0005 asks whether the market state is better described by a richer context than the immediately previous b… A human looking at a chart does not only remember the last touch or the last exit. A human sees that the market has been behaving in a continuation-heavy or reversal-heavy way for a local period. The human eye naturally… H0005 formalizes that intuition with a past-only context vector. For each event `i`, H0005/M0004-v1.03 can compute: The current event's label is never used to construct its own context. The research must keep both views: This keeps H0004 interpretable while allowing H0005 to become a state-machine research layer. The most important H0005 test is the conflict test: If context wins in conflict cases, then the

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0002, H0003, H0004, H0005, M0004

## Headings

- H0005 — Contextual Branch Regime State
  - Research question
  - Why this is closer to human perception
  - Past-only context vector
  - Two-mode design
  - Main decision metric
  - Context quality metrics
  - Stress requirements
  - Strategy relevance
  - Consensus state — lastBranch + human-eye context
  - Consensus quality layer — v1.04
    - Core distinction

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `33`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `33`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `33`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `33`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005_contextual_branch_regime_state.md]] — score `33`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001_structural_highs_lows_as_decision_nodes.md]] — score `32`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `28`
- [[README|README.md]] — score `27`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `25`
- [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]] — score `25`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
