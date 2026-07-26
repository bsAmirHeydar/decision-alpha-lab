
---
type: source_card
source_path: "docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md"
source_ext: ".md"
source_size: 11100
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "H0003", "H0004", "M0001", "M0002", "M0003", "M0004"]
---

# Source Card — H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md

## Source

[[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]]

## Summary

Version: 1.75 This document is the logic lock for the first two Decision Alpha Lab hypotheses. It is written as a research README, not as a strategy guide. The goal is to make every algorithmic assumption explicit enough that future r… M0002 does not create a separate event stream. It receives the exact completed events produced by M0001 and only labels them by the side of the completed exit candle relative to the original node price. Do rule-based structural highs/lows produce higher event-window volatility than matched random windows? A node is defined by the L-rule. The pivot candle is the visual marker, but logic starts only after the right-side confirmation exists. No event may start before `active_from_index`. This is the lookahead guard. The node price is the anchor. The live expansion extreme updates while the node is alive. Territory is built around the original node price: A to

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, H0003, H0004, M0001, M0002, M0003, M0004

## Headings

- H0001 / H0002 Algorithm and Hypothesis README
  - Current research stack
  - H0001 — Structural node relative territory volatility
    - Research question
    - Structural nodes
    - Live territory construction
    - Touch event
    - Exit logic
    - Consumption mode
    - RTV measurement
    - Random null model
    - H0001 acceptance pattern

## Related Source Documents

- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `53`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `53`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `48`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005_contextual_branch_regime_state.md]] — score `48`
- [[README|README.md]] — score `45`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `43`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `43`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `36`
- [[docs/evidence/h0001_structural_highs_lows_as_decision_nodes/a8381ae9b922_H0001_structural_highs_lows_as_decision_nodes|H0001_structural_highs_lows_as_decision_nodes.md]] — score `35`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `34`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
