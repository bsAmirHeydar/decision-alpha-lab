
---
type: source_card
source_path: "docs/mql_native/H0001_H0004_RESEARCH_LOCK.md"
source_ext: ".md"
source_size: 8146
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "H0003", "H0004", "M0001", "M0002", "M0003", "M0004"]
---

# Source Card — H0001_H0004_RESEARCH_LOCK.md

## Source

[[docs/mql_native/H0001_H0004_RESEARCH_LOCK|docs/mql_native/H0001_H0004_RESEARCH_LOCK.md]]

## Summary

This document audits the first four MQL-native Decision Alpha Lab hypotheses as one layered research stack. It answers two questions: Are the four implemented hypotheses the same hypotheses that were discussed? What still remains open before these facts can be converted into a trading strategy? Current active build targets in this snapshot: M0001 is the base event engine. M0002, M0003, and M0004 must not build independent event universes. They inherit completed M0001 events and M0002 branch labels. A report is part of the locked stack only if it respects these guards: Forbidden old semantics: Structural highs/lows are not arbitrary points. Completed node-territory touch events should have higher relative territory volatility than matched random windows. H0001 matches the intended hypothesis. It is a market-structure volatility fact candidate, not a directional strategy. After a completed

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, H0003, H0004, M0001, M0002, M0003, M0004

## Headings

- H0001-H0004 Research Lock
  - Runtime target map
  - Non-negotiable stack guard
  - H0001 — Structural node volatility fact
    - Intended hypothesis
    - Implemented algorithm
    - Status
  - H0002 — Branch volatility model
    - Intended hypothesis
    - Implemented algorithm
    - Branch definition
    - Status

## Related Source Documents

- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `53`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `53`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `48`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005_contextual_branch_regime_state.md]] — score `48`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `43`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `43`
- [[README|README.md]] — score `37`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `36`
- [[lab/02_hypotheses/H0001_structural_highs_lows_as_decision_nodes|H0001_structural_highs_lows_as_decision_nodes.md]] — score `35`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `34`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
