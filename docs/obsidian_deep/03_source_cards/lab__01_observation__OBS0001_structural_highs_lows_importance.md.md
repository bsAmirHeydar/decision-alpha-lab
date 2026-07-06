
---
type: source_card
source_path: "lab/01_observation/OBS0001_structural_highs_lows_importance.md"
source_ext: ".md"
source_size: 2248
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Rally"]
entities: ["H0001"]
---

# Source Card — OBS0001_structural_highs_lows_importance.md

## Source

[[lab/01_observation/OBS0001_structural_highs_lows_importance|lab/01_observation/OBS0001_structural_highs_lows_importance.md]]

## Summary

Throughout the development, testing, and manual execution of multiple trading approaches, a recurring pattern was observed: Strategies that ignored prior structural highs and lows generally exhibited poor practical performance. Conversely, strategies that explicitly incorporated these structures often produced better trading outcomes. However, these improvements were not sufficiently stable, objective, or systematic to justify full automation. This observation emerged from repeated interaction with the market rather than from formal statistical analysis. It reflects accumulated practical experience rather than established evidence. The following recurring phenomena were noted around prior structural highs and lows: Not all price locations appeared equally important. Historical highs and lows frequently coincided with meaningful changes in market behavior. Ignoring these structures often

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Rally|Rally]]

## Entities

H0001

## Headings

- OBS0001 — Apparent Importance of Structural Highs and Lows
  - Observation
  - Context
  - What Was Observed
  - What Is NOT Claimed
  - Motivation

## Related Source Documents

- [hypotheses.yaml](../../registry/hypotheses.yaml) — score `15`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `11`
- [[lab/02_hypotheses/H0001_structural_highs_lows_as_decision_nodes|H0001_structural_highs_lows_as_decision_nodes.md]] — score `11`
- [[lab/02_hypotheses/H0002_structural_node_revisitation|H0002_structural_node_revisitation.md]] — score `11`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `9`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `9`
- [[docs/mql_native/H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE|H0001_MARKET_STRUCTURE_VOLATILITY_ARTICLE.md]] — score `9`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `9`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `9`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `9`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
