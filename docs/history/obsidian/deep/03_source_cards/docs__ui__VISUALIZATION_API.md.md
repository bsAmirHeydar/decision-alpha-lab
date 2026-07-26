
---
type: source_card
source_path: "docs/ui/VISUALIZATION_API.md"
source_ext: ".md"
source_size: 5226
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["EXP0001", "H0001", "H0002", "M0001"]
---

# Source Card — VISUALIZATION_API.md

## Source

[[docs/ui/VISUALIZATION_API|docs/ui/VISUALIZATION_API.md]]

## Summary

This document defines the data contract between the Python research backend and the React visual terminal. Every metric and experiment must describe its visual output using these generic contracts instead of building metric-specific UI components. A replay visualization response should return: Allowed `source` values: The chart must render candles from this contract only. Allowed layer types: A table row must include a `selection_ref`: Selection must be deterministic and bidirectional. M0001 must eventually provide an adapter that maps metric output rows into: The metric itself should not import UI code. The adapter lives in `apps/api/app/services/visualization_mapper.py` or a metric-specific mapper under the API layer. Every visualization payload must include: Breaking changes require a new version.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

EXP0001, H0001, H0002, M0001

## Headings

- Visualization API Contract
  - Purpose
  - Top-Level Response
  - Dataset Descriptor
  - Candle Contract
  - Overlay Layer Contract
  - Marker Object
  - Zone Object
  - Event Window Object
  - Table Contract
  - Selection Map
  - Inspector Payload

## Related Source Documents

- [[docs/ui/ROADMAP|ROADMAP.md]] — score `35`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `29`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `27`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `27`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `27`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `27`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `27`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `27`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002_DEEP_AUDIT_AND_STABILITY.md]] — score `27`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `27`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
